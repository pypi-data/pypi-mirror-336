import asyncio
import inspect
import logging
import uuid
import os
from datetime import datetime
import sys
import threading
from contextvars import ContextVar
from logging.handlers import TimedRotatingFileHandler

from fastapi.routing import APIRoute

# 自定义trace_filter属性名
TRACE_FILTER_ATTR = "trace_filter"
# 当前线程的local_trace, 需要添加全局trace_id, 使用示例：trace.trace_id
local_trace = threading.local()
formatter = logging.Formatter(
    '%(asctime)s \t %(trace_id)s \t %(name)s \t %(levelname)s \t %(message)s')
_trace_id: ContextVar[str] = ContextVar('x_trace_id', default="-")
_x_request_id: ContextVar[str] = ContextVar('_x_request_id', default="-")

# 自定义日志格式器，用于格式化包含根方法路径的日志消息
class CustomFormatter(logging.Formatter):
    def format(self, record):
        # 定义自定义格式字符串，包含根方法路径
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(root_method_path)s - %(message)s'
        return super().format(record, format_string)


class TraceID:
    @staticmethod
    def set(req_id: str) -> ContextVar[str]:
        """设置请求ID，外部需要的时候，可以调用该方法设置
        Returns:
            ContextVar[str]: _description_
        """
        if req_id:
            _x_request_id.set(req_id)
        return _x_request_id

    @staticmethod
    def set_trace(trace_id: str) -> ContextVar[str]:
        """设置trace_id
        Returns:
            ContextVar[str]: _description_
        """
        if trace_id:
            _trace_id.set(trace_id)
        return _trace_id

    @staticmethod
    def new_trace():
        trace_id = uuid.uuid4().hex
        _trace_id.set(trace_id)

    @staticmethod
    def get_trace() -> str:

        """获取trace_id
        Returns:
            str: _description_
        """
        return _trace_id.get()


class TraceFilter(logging.Filter):
    """
    通过在record中添加trace_id, 实现调用跟踪和日志打印的分离
    """

    def __init__(self, name=""):
        """
        init
        @param name: filter name
        """
        super().__init__(name)

    def filter(self, record):
        """
        重写filter方法
        @param record: record
        @return:
        """
        # trace_id = local_trace.trace_id if hasattr(local_trace, 'trace_id') else uuid.uuid1()
        record.trace_id = _trace_id.get()
        return True

class TraceLogger:
    _loggers = {}
    @staticmethod
    def get_log_file_path(logger_name):
        log_dir_name = 'logs'
        current_working_directory = os.getcwd()
        log_dir = os.path.join(current_working_directory, log_dir_name)
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        log_file_name = "{}_log.{}.log".format( logger_name, str(datetime.now().strftime('%Y-%m-%d')))
        log_file_path = os.path.join(log_dir, log_file_name)
        return log_file_path
    @staticmethod
    def get_logger_func(logger_name,config):
        if logger_name in TraceLogger._loggers:
            return TraceLogger._loggers[logger_name]
        # 创建一个名为'access'的日志记录器实例
        access_logger = logging.getLogger(logger_name)
        # 设置日志记录器的最低捕获级别
        access_logger.setLevel(config['logger_level'])
        # 避免重复添加过滤器
        if not any(isinstance(f, TraceFilter) for f in access_logger.filters):
            # 添加日志跟踪过滤器
            trace_filter = TraceFilter()
            access_logger.addFilter(trace_filter)
        access_filename = TraceLogger.get_log_file_path(logger_name)
        if access_filename:
            # 避免重复添加文件处理器
            if not any(isinstance(h, TimedRotatingFileHandler) for h in access_logger.handlers):
                # 创建一个按时间滚动的文件处理器
                file_handler = TimedRotatingFileHandler(
                    access_filename,
                    when=config['acc_when'],
                    backupCount=config["backupCount"],
                    encoding='utf-8'
                )
                # 设置文件处理器的格式化器
                file_handler.setFormatter(formatter)
                # 将文件处理器添加到日志记录器中
                access_logger.addHandler(file_handler)
        if config['is_console']:
            # 避免重复添加控制台处理器
            if not any(isinstance(h, logging.StreamHandler) for h in access_logger.handlers):
                # 再创建一个handler，用于将日志输出到控制台
                console_handler = logging.StreamHandler()
                console_handler.setLevel(config['console_level'])  # 设置控制台handler的日志级别
                console_handler.setFormatter(formatter)
                access_logger.addHandler(console_handler)
        TraceLogger._loggers[logger_name] = access_logger
        return access_logger

# 定义日志记录器
def create_loggers(config):
    acc_config = config['access']
    server_config = config['server']
    err_config = config['error']
    info_config = config['all_info']
    acc_logger = TraceLogger.get_logger_func("access", config=acc_config)
    server_logger = TraceLogger.get_logger_func("server", config=server_config)
    error_logger = TraceLogger.get_logger_func("error",config=err_config)
    all_info = TraceLogger.get_logger_func("info", config=info_config)
    return acc_logger, server_logger, error_logger,all_info

def get_module_line(e: any,project_path=None):
    # tb = e.__traceback__
    # # 遍历到最内层的调用栈
    # while tb.tb_next:
    #     tb = tb.tb_next
    #
    # # 获取真正出错的模块名
    # module_name = tb.tb_frame.f_code.co_filename.split("/")[-1].replace(".py", "")
    # # 获取出错行号
    # line_number = tb.tb_lineno
    # # 获取出错方法名
    # method_name = tb.tb_frame.f_code.co_name
    #
    # module_line = "{}.{}".format(module_name, method_name, line_number)
    # return module_line

    # 解析堆栈信息
    relative_path = '-'
    module_path = '-'
    stack_lines = e.strip().split('\n')
    project_root = project_path if  project_path else os.getcwd()  # 假设项目根目录为当前工作目录
    for line in stack_lines:
        if line.startswith('  File'):
            parts = line.split('"')
            if len(parts) > 1:
                file_path = parts[1]
                if file_path.startswith(project_root):
                    relative_path = os.path.relpath(file_path, project_root)
                    module_path = relative_path.replace(os.sep, '.')[:-3]  # 去除 .py 扩展名
                    # 从 parts 中进一步提取方法名
                    function_part = parts[-1].strip()
                    if function_part.startswith(', line'):
                        sub_parts = function_part.split(',')
                        if len(sub_parts) > 2 and sub_parts[2].strip().startswith('in '):
                            function_name = sub_parts[2].strip().split(' ')[-1]
    return f"{module_path}.{function_name}"


def get_process_funcname(app, request):
    moduler_func_line = None
    func_module, func_name, func_line = None, None, None
    try:
        for route in app.routes:
            if route.path.startswith("/docs") or route.path.startswith("/redoc") or route.path.startswith("/openapi.json"):
                continue
            match, matched_path_params = route.matches(request.scope)
            if match:
                methods = set()
                if isinstance(route, APIRoute):
                    methods = route.methods

                if request.method.lower() in [method.lower() for method in methods]:
                #     print(f"匹配到的路由路径: {route.path}")  # 调试信息
                    # func_name = route.endpoint.__name__
                    if request.scope.get('path') == route.path:
                        endpoint = route.endpoint
                        func_name = endpoint.__name__ if hasattr(endpoint, '__name__') else str(endpoint)
                    else:
                        continue
                    try:
                        source_lines, start_line = inspect.getsourcelines(route.endpoint)
                        func_line = start_line
                        module = inspect.getmodule(route.endpoint)
                        if module:
                            full_module_name = module.__name__
                            if '.' in full_module_name:
                                func_module = full_module_name.split('.')[-1]
                            else:
                                func_module = full_module_name
                        else:
                            func_module = "无法获取模块"
                    except (TypeError, OSError) as e:
                        pass
                    break
    except Exception as e:
        pass
    if func_module and func_name and func_line:
        moduler_func_line = "{}.{}".format(func_module, func_name)
    return moduler_func_line


def get_main_tracebak(stack_trace,project_path=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 定义你的项目路径
    project_path = project_path if project_path else os.getcwd()

    # 分割堆栈跟踪信息为行
    lines = stack_trace.splitlines()

    # 提取主要堆栈内容
    main_stack = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if project_path in line:
            main_stack.append(line)
            if i + 1 < len(lines):
                main_stack.append(lines[i + 1])
            i += 2  # 跳过下一行，因为已经添加了
        else:
            i += 1
    # 打印主要堆栈内容
    main_tracebak = ''.join(main_stack).replace('\t','').replace('\n','') + lines[-1] if len(lines) > 0 else ''
    return main_tracebak

def clean_error_message(error_message):
    # 将换行符替换为空格
    error_message = error_message.replace('\n', ' ')
    # 将制表符替换为空格
    error_message = error_message.replace('\t', ' ')
    # 将两个及以上的连续空格替换为一个空格
    while '  ' in error_message:
        error_message = error_message.replace('  ', ' ')
    return error_message

async def get_params(request):
    # 获取 URL 中的参数
    query_params = dict(request.query_params) if request else {}
    params = {}
    if query_params:
        params['query_params'] = query_params
    content_type = request.headers.get('Content-Type', '')
    if 'multipart/form-data' in content_type:
        # 处理包含文件上传的表单数据
        try:
            form = await asyncio.wait_for(request.form(), timeout=10)
            has_file = False
            filename = '-'
            for field_name, value in form.items():
                if hasattr(field_name, 'filename'):
                    has_file = True
                    filename = value.filename
                    break
            if has_file:
                params['file'] = filename
            else:
                params['form'] = await request.form()
        except asyncio.TimeoutError:
            form = "上传大文件"
            params['form'] = form

    elif 'application/x-www-form-urlencoded' in content_type:
        params['form'] = await request.form()
    elif 'application/json' in content_type:
        body_params = await request.json()
        params['body_params'] = body_params
    else:
        params['others'] = ""
    return params