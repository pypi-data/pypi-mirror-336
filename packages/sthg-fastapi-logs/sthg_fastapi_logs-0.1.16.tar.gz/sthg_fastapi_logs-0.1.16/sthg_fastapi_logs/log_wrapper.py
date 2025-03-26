import asyncio
import inspect
import logging
import os
import time
import functools
import traceback
import json
from starlette.responses import StreamingResponse

from sthg_fastapi_logs.utils.code_utils import handle_method_status, handle_business_code, get_main_traceback
from sthg_fastapi_logs.utils.exception_utils import CustomException
from .enumerate import CodeEnum, HttpStatusCode, RESULT_SUCCESS, BusinessCode
from .log_util import TraceID, local_trace, create_loggers, get_module_line, get_process_funcname, get_main_tracebak, \
    clean_error_message

TOKEN_URL = 'http://192.168.1.243:9103/api/user/userInfoByToken'


def get_process_time(start_time, end_time):
    return '{}'.format(round((end_time - start_time) * 1000, 6))


def get_status(response):
    if hasattr(response, 'status_code'):
        return identify_code(response.status_code)
    return CodeEnum.SUCCESS


def get_trace_id():
    if hasattr(local_trace, 'trace_id'):
        return local_trace.trace_id
    return ''


def get_request_method(request):
    return str(request.url)


def get_ip(request):
    return request.client.host


def get_header(request):
    return dict(request.headers)


async def get_request_params(request):
    params = dict(request.query_params) if request.query_params else "-"
    if not params:
        byte_body = await request.body()
        params = json.loads(byte_body.decode()) if byte_body else "-"
    return params


async def get_response(response):
    # 如果响应是一个 StreamingResponse，我们需要特殊处理
    if isinstance(response, StreamingResponse):
        # 我们需要创建一个新的 StreamingResponse
        # 并且修改它的响应体
        async def new_streaming_response(stream):
            async for chunk in stream:
                # 在这里可以处理每个 chunk，例如记录日志、修改内容等
                yield chunk  # 发送 chunk

        return StreamingResponse(new_streaming_response(response.body_iterator), media_type=response.media_type)
    else:
        # 对于非 StreamingResponse，可以直接修改 response.body
        data = await response.body()
        modified_data = data  # 在这里可以修改数据
        return Response(modified_data, media_type=response.media_type, status_code=response.status_code)
    # return data


def identify_code(code):
    code = int(code)
    ranges = {
        CodeEnum.SUCCESS.value: (199, 207),
        CodeEnum.REEOR.value: (1, 1),
        CodeEnum.PARAM_ERROR.value: (400, 499),
        CodeEnum.INNER_REEOR.value: (500, 10000)
        # 可以添加更多的范围
    }

    for identifier, (start, end) in ranges.items():
        if start <= code <= end:
            return identifier
    # 特殊的 code 处理
    if 0 <= code <= 0:
        return CodeEnum.SUCCESS.value
    return CodeEnum.SUCCESS.value


def get_response_code(response):
    # 拿到 code
    if response and type(response) == dict:
        code = response.get('code') or response.get('Code') or response.get('CODE')
    else:
        code = "-"
    # 转换 code
    if code:
        code = identify_code(code)
    else:
        code = CodeEnum.SUCCESS.value
    return code


def get_response_msg(response):
    if response and type(response) == dict:
        msg = response.get('msg') or response.get('message') or response.get('Message')
    else:
        msg = "-"
    return msg


def get_response_data(response):
    if response and type(response) == dict:
        msg = response
    else:
        msg = "-"
    return msg


def get_request_data(args, kwargs):
    params = {
        'args': args[1:],
        'kwargs': kwargs
    }
    if not params:
        params = '-'
    return params


"""
"time":请求时间
,"traceId":全链路Id
,"method":访问方法
,"status":http状态码
,"code":业务状态码
,"msg": 返回描述，当异常时，可以把简略堆栈放里面
,"resRT": 响应时长
,"logRT": 日志打印耗时
,"guid": 留空
,"requestId":用户访问唯一码
,"userId": 用户id
,"extObj": 扩展信息：包含用Ip,和请求header
,"reqParams": 请求参数
,"reData": 返回参数
"""
from fastapi import (
    FastAPI,
    Request,
    Response
)


# 依赖函数，用于获取所有类型的参数
async def request_params(request):
    # # 路径参数
    path_params = request.path_params
    # 查询参数
    query_params = dict(request.query_params)

    content_type = request.headers.get('content-type') if request.headers.get('content-type') else ''
    # 表单数据
    form_data = {}
    #不可识别数据
    others = ''
    # 请求体数据
    body_data = {}
    try:
        if content_type and 'application/json' in content_type:
            body_data = await request.body()
            body_data = json.dumps(body_data.decode())
        elif content_type and 'multipart/form-data' in content_type:
            if 'multipart/form-data; boundary=' in content_type:
                form = await asyncio.wait_for(request.form(), timeout=10)
                has_file = False
                filename = '-'
                for field_name, value in form.items():
                    if hasattr(field_name, 'filename'):
                        has_file = True
                        break
                if has_file:
                    form_data["file_upload"] = 1
                else:
                   form = await request.form()
                   form_data = {key: value for key, value in form.items()}
            else:
                form = await request.form()
                form_data = {key: value for key, value in form.items()}
        elif content_type and 'application/x-www-form-urlencoded' in content_type:
            form = await request.form()
            form_data = {key: value for key, value in form.items()}
        else:
            others = '-'
    except Exception as e:
        pass
    params_input = {}
    if query_params:
        params_input['params'] = query_params
    if form_data:
        params_input['form_data'] = form_data
    if body_data:
        params_input['body'] = body_data
    if others:
        params_input['others'] = others
    return params_input


# 声明全局变量
default_config = {
    "access": {
        "is_console": False,
        "is_msg": False,
        "is_request": False,
        "is_response": False,
        "logger_level": logging.DEBUG,
        "console_level": logging.INFO,
        "acc_when": "W6",
        "backupCount": 0
    },
    "error": {
        "is_console": False,
        "is_msg": False,
        "is_request": False,
        "is_response": False,
        "logger_level": logging.ERROR,
        "console_level": logging.ERROR,
        "acc_when": "W6",
        "backupCount": 0
    },
    "all_info": {
        "is_console": False,
        "is_msg": False,
        "is_request": False,
        "is_response": False,
        "logger_level": logging.INFO,
        "console_level": logging.INFO,
        "acc_when": "W6",
        "backupCount": 0
    },
    "server": {
        "is_console": False,
        "is_msg": False,
        "is_request": False,
        "is_response": False,
        "logger_level": logging.DEBUG,
        "console_level": logging.INFO,
        "acc_when": "W6",
        "backupCount": 0
    }
}


def init_log_config(config: dict[str, dict] = None):
    global default_config,acc_logger, server_logger, error_logger, all_info
    if config:
        for k, v in config.items():
            default_config[k] = v
    acc_logger, server_logger, error_logger, all_info = create_loggers(default_config)


def get_module_func_by_router(request):
    route = request.scope.get("route")
    if route:
        endpoint = route.endpoint
        # 获取函数的定义信息
        source_lines, start_line = inspect.getsourcelines(endpoint)
        method_name = endpoint.__name__
        module_file = inspect.getmodule(endpoint).__file__
        return module_file, method_name, start_line
    else:
        raise Exception('route not found')


def register_log_middleware(app: FastAPI):
    # 全局变量,以便通过中间件引入,可以进行配置


    @app.middleware("http")
    async def log_middleware(request: Request, call_next):
        start_time = time.time()
        _request_id_key = "X-Request-Id"
        _trace_id_key = "X-Request-Id"
        _trace_id_val = request.headers.get(_trace_id_key)
        if _trace_id_val:
            TraceID.set_trace(_trace_id_val)
            TraceID.set_trace(_trace_id_val)
        else:
            TraceID.new_trace()
            _trace_id_val = TraceID.get_trace()
        local_trace.trace_id = TraceID.get_trace()
        local_trace.request = request
        moduler_func_line = get_process_funcname(app, request)

        # content_type = request.headers.get('content-type', '')


        async  def set_body(request: Request):
            receive_ = await  request._receive()
            async def receive():
                return receive_
            request._receive = receive

        await set_body(request)

        param_input = await request_params(request)
        if not param_input:
            param_input = "-"

        try:
            response = await call_next(request)

            process_time = get_process_time(start_time, time.time())
            log_time_start = time.time()

            msg = get_response_msg(response)
            status_code = handle_method_status(response.status_code)
            code = handle_business_code(response.status_code)
            body = b""
            if hasattr(response, "body_iterator"):
                async for chunk in response.body_iterator:
                    body += chunk
            try:
                # 将字节类型的 body 解码为字符串，再解析为 JSON 对象
                json_data = json.loads(body.decode('utf-8'))

            except json.JSONDecodeError:
                # 处理 JSON 解析错误
                json_data = '-'

            if status_code != "SUCCESS":
                if type(json_data) is dict:
                    msg = get_response_msg(json_data)
                    module_file, method_name, start_line = get_module_func_by_router(request)
                    msg = f'Traceback (most recent call last):\nFile\t"{module_file}",\tline{start_line},\tin\t{method_name}\traise\tException({msg})'
                json_data = '-'

            info_kwargs = {
                'request': request,
                'process_time': process_time,
                "status_code": status_code,
                "code": code,
                'return_desc': HttpStatusCode.get_description(response.status_code),
                'msg': msg,
                'moduler_func_line': moduler_func_line,
                'param_input': param_input,
                'respData': json_data if json_data else '_',
                "log_time_start": log_time_start
            }
            await get_all_info_log_str(**info_kwargs)
            # 重新创建响应对象
            new_response = Response(content=body, status_code=response.status_code, headers=dict(response.headers))
            new_response.headers["X-Request-Id"] = str(_trace_id_val)
            new_response.headers["X-Process-Time"] = str(process_time)
            return new_response
        except AttributeError as e:
            process_time = get_process_time(start_time, time.time())
            log_time_start = time.time()
            # 获取当前请求对应的路由处理函数
            module_file, method_name, start_line = get_module_func_by_router(request)
            custom_stack = f'Traceback (most recent call last):\nFile\t"{module_file}",\tline{start_line},\tin\t{method_name}\traise\tAttributeError({e})'

            status_code = handle_method_status(500)
            code = handle_business_code(500)
            info_kwargs = {
                'request': request,
                'process_time': process_time,
                "status_code": status_code,
                "code": code,
                'return_desc': HttpStatusCode.get_description(500),
                'msg': custom_stack,
                'moduler_func_line': moduler_func_line,
                'param_input': param_input,
                'respData': '-',
                "log_time_start": log_time_start
            }
            await get_all_info_log_str(**info_kwargs)
            raise e

        except Exception as e:
            process_time = get_process_time(start_time, time.time())
            log_time_start = time.time()
            status_code = handle_method_status(500)
            code = handle_business_code(500)
            msg = get_main_traceback(traceback.format_exc())
            module_file, method_name, start_line = get_module_func_by_router(request)
            custom_stack = f'Traceback (most recent call last):\nFile\t"{module_file}",\tline{start_line},\tin\t{method_name}\traise\tException({e})'
            info_kwargs = {
                'request': request,
                'process_time': process_time,
                "status_code": status_code,
                "code": code,
                'return_desc': HttpStatusCode.get_description(500),
                'msg': custom_stack,
                'moduler_func_line': moduler_func_line,
                'param_input': param_input,
                'respData': '-',
                "log_time_start": log_time_start
            }
            await get_all_info_log_str(**info_kwargs)
            raise e


# 记录api执行日志
def access_log(**access_kwargs):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            # 尝试从参数中获取 Request 对象
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if not request:
                request = local_trace.request

            params = await request_params(request)
            moduler_func_line = ''
            return_desc = '-'
            try:
                # 获取code
                msg = "-"
                request = local_trace.request
                method_name = func.__name__
                module = inspect.getmodule(func)
                if module is not None and hasattr(module, '__file__'):
                    # 获取模块对应的文件路径
                    project_root = os.getcwd()
                    # current_dir = os.path.dirname(os.path.abspath(project_root))
                    module_file = module.__file__
                    relative_path = os.path.relpath(module_file, project_root)
                    module_path = relative_path.replace(os.sep, '.')[:-3]  # 去除 .py 扩展名
                    new_module_path = module_path.split('.')[-1]
                    moduler_func_line = "{}.{}".format(new_module_path, method_name)

                if asyncio.iscoroutinefunction(func) or 'function' not in str(type(func)):
                    response = await func(*args, **kwargs)
                    if response and not isinstance(response, dict):
                        response = await response
                else:
                    response = func(*args, **kwargs)
                process_time = get_process_time(start_time, time.time())
                log_time_start = time.time()

                if isinstance(response, dict):
                    if 'code' in response or 'http_code' in response:
                        if 'code' in response:
                            code = response['code']
                        else:
                            code = response['http_code']
                    else:
                        raise CustomException("返回结构不是标准结构")
                else:
                    raise CustomException("返回结构不是标准结构")

                status_code = handle_method_status(code)
                busiCode = handle_business_code(code)
                if code in [0, 1]:
                    if code == 0:
                        return_desc = f"请求成功"
                    if code == 1:
                        return_desc = f"请求失败"
                else:
                    return_desc = HttpStatusCode.get_description(code)

                access_info = {
                    'request': request,
                    'process_time': process_time,
                    "status_code": status_code,
                    "code": busiCode,
                    'return_desc': return_desc,
                    'msg': msg,
                    'moduler_func_line': moduler_func_line,
                    'param_input': params,
                    'respData': response if response else '-',
                    "log_time_start": log_time_start
                }
                await get_access_log_str(**access_info)
            except CustomException as e:
                process_time = get_process_time(start_time, time.time())
                log_time_start = time.time()
                file_path = inspect.getfile(func)
                # 获取文件所在的目录路径
                current_dir = os.path.dirname(os.path.abspath(file_path))
                moduler_func_line = moduler_func_line if moduler_func_line else get_module_line(traceback.format_exc(),
                                                                                                project_path=current_dir)
                _, start_line = inspect.getsourcelines(func)
                custom_stack = f'Traceback (most recent call last):\nFile\t"{module_file}",\tline{start_line},\t in\t{method_name}\traise CustomException("{e}")'
                request = local_trace.request
                access_info = {
                    'request': request,
                    'process_time': process_time,
                    "status_code": 'SUCCESS',
                    "code": 'InnerError',
                    'return_desc': HttpStatusCode.get_description(500),
                    'msg': custom_stack,
                    'moduler_func_line': moduler_func_line,
                    'param_input': params,
                    'respData': '-',
                    "log_time_start": log_time_start
                }
                await get_access_log_str(**access_info)
                raise CustomException(custom_stack)
            except ValueError as e:
                process_time = get_process_time(start_time, time.time())
                log_time_start = time.time()
                file_path = inspect.getfile(func)
                # 获取文件所在的目录路径
                current_dir = os.path.dirname(os.path.abspath(file_path))
                moduler_func_line = moduler_func_line if moduler_func_line else get_module_line(traceback.format_exc(),
                                                                                                project_path=current_dir)
                msg = get_main_traceback(traceback.format_exc())
                request = local_trace.request
                response = Response(status_code=500)
                access_info = {
                    'request': request,
                    'process_time': process_time,
                    "status_code": handle_method_status(response.status_code),
                    "code": handle_business_code(response.status_code),
                    'return_desc': HttpStatusCode.get_description(response.status_code),
                    'msg': msg,
                    'moduler_func_line': moduler_func_line,
                    'param_input': params,
                    'respData': '-',
                    "log_time_start": log_time_start
                }
                await get_access_log_str(**access_info)
                raise ValueError(e)
            except Exception as exc:
                process_time = get_process_time(start_time, time.time())
                log_time_start = time.time()
                file_path = inspect.getfile(func)
                # 获取文件所在的目录路径
                current_dir = os.path.dirname(os.path.abspath(file_path))

                moduler_func_line = moduler_func_line if moduler_func_line else get_module_line(traceback.format_exc(),
                                                                                                project_path=current_dir)
                exc_type = type(exc)
                exc_value = exc
                exc_tb = exc.__traceback__
                # 调用 format_exception 函数格式化异常信息
                formatted_exception = traceback.format_exception(exc_type, exc_value, exc_tb)
                # 打印格式化后的异常信息
                main_error = "Traceback (most recent call last):\n" + get_main_tracebak(''.join(formatted_exception),
                                                                                        project_path=current_dir)
                #
                request = local_trace.request
                response = Response(status_code=500)
                access_info = {
                    'request': request,
                    'process_time': process_time,
                    "status_code": 'ERROR',
                    "code": 'InnerError',
                    'return_desc': HttpStatusCode.get_description(response.status_code),
                    'msg': main_error,
                    'moduler_func_line': moduler_func_line,
                    'param_input': params,
                    'respData': '-',
                    "log_time_start": log_time_start
                }
                await get_access_log_str(**access_info)
                raise exc
            return response

        return wrapper

    return decorator


"""
"time":请求时间
,"traceId":全链路Id
,"method":访问方法
,"status":http状态码
,"code":业务状态码
,"msg": 返回描述，当异常时，可以把简略堆栈放里面
,"resRT": 响应时长
,"logRT": 日志打印耗时
,"reqParams": 请求参数
,"reData": 返回参数
"""


# 记录方法执行日志
def service_log():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            msg = '-'
            params = get_request_data(args, kwargs)
            method_name = func.__name__
            module = inspect.getmodule(func)
            if module is not None and hasattr(module, '__file__'):
                # 获取模块对应的文件路径
                project_root = os.getcwd()
                module_file = module.__file__
                relative_path = os.path.relpath(module_file, project_root)
                module_path = relative_path.replace(os.sep, '.')[:-3]  # 去除 .py 扩展名
                new_module_path = module_path.split('.')[-1]
                moduler_func_line = "{}.{}".format(new_module_path, method_name)
            start_time = time.time()

            if asyncio.iscoroutinefunction(func) or 'function' not in str(type(func)):
                response = await func(*args, **kwargs)
                if not isinstance(response, dict):
                    response = await response
            else:
                response = func(*args, **kwargs)
            process_time = get_process_time(start_time, time.time())
            log_time_start = time.time()
            reData = get_response_data(response)
            if not params: params = '-'
            await get_service_log_str(moduler_func_line, process_time, log_time_start, RESULT_SUCCESS, "OK",
                                      "业务处理成功",
                                      msg, params, reData)
            return response

        return wrapper

    return decorator


#
def class_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        msg = "-"
        reData = '-'
        params = get_request_data(args, kwargs)

        method_name = func.__name__
        module = inspect.getmodule(func)
        if module is not None and hasattr(module, '__file__'):
            # 获取模块对应的文件路径
            project_root = os.getcwd()
            current_dir = os.path.dirname(os.path.abspath(project_root))
            module_file = module.__file__
            relative_path = os.path.relpath(module_file, current_dir)
            module_path = relative_path.replace(os.sep, '.')[:-3]  # 去除 .py 扩展名
            new_module_path = module_path.split('.')[-1]
            moduler_func_line = "{}.{}".format(new_module_path, method_name)
        start_time = time.time()
        response = func(*args, **kwargs)
        process_time = get_process_time(start_time, time.time())
        log_time_start = time.time()
        reData = response if response else reData
        await get_service_log_str(moduler_func_line, process_time, log_time_start, "SUCCESS", 'OK', '业务处理成功', msg,
                                  params, reData)
        return response

    return wrapper


def class_log(cls):
    for name, method in vars(cls).items():
        if callable(method) and name != '__init__':  # 排除__init__方法
            setattr(cls, name, class_decorator(method))
    return cls


async def get_access_log_str(**access_kwargs):
    # acc_logger, server_logger, error_logger, all_info = create_loggers(default_config)
    try:
        request = access_kwargs['request']
        request_header = get_header(request)
        guid = request_header.get('X-GUID') if request_header.get('X-GUID') else "-"
        requestId = TraceID.get_trace() if TraceID.get_trace() else "-"
        userId = request_header.get('X-User-ID') if request_header.get('X-User-ID') else "-"
        header = {"user_ip": get_ip(request), "host": request_header['host'], 'user_id': userId}
        msg = clean_error_message(access_kwargs['msg'])
        moduler_func_line = str(access_kwargs['moduler_func_line']).replace('...', '')
        status_code = access_kwargs['status_code']
        code = access_kwargs['code']
        return_desc = access_kwargs['return_desc']
        process_time = access_kwargs['process_time']
        param_input = access_kwargs['param_input']
        respData = access_kwargs['respData']
        log_time_start = access_kwargs['log_time_start']
        logRT = get_process_time(log_time_start, time.time())
        info_msg = f"""{moduler_func_line}\t {status_code}\t {code}\t {return_desc}\t {process_time}\t {logRT}\t {guid}\t {userId}\t {requestId}\t header-{header}\t {param_input}\t {respData}\t {msg}"""

        acc_logger.info(str(info_msg))
    except Exception as e:
        error_logger.error('access log error :{}'.format(str(e)))


async def get_all_info_log_str(**info_kwargs):
    # acc_logger, server_logger, error_logger, all_info = create_loggers(default_config)
    try:
        request = info_kwargs['request']
        request_header = get_header(request)
        guid = request_header.get('X-GUID') if request_header.get('X-GUID') else "-"
        requestId = TraceID.get_trace() if TraceID.get_trace() else "-"
        userId = request_header.get('X-User-ID') if request_header.get('X-User-ID') else "-"
        header = {"user_ip": get_ip(request), "host": request_header['host'], 'user_id': userId}
        moduler_func_line = str(info_kwargs['moduler_func_line']).replace('...', '')
        status_code = info_kwargs['status_code']
        code = info_kwargs['code']
        process_time = info_kwargs['process_time']
        msg = clean_error_message(info_kwargs['msg'])
        param_input = info_kwargs['param_input']
        respData = info_kwargs['respData']
        return_desc = info_kwargs['return_desc']
        log_time_start = info_kwargs['log_time_start']
        logRT = get_process_time(log_time_start, time.time())
        info_msg = f"""{moduler_func_line}\t {status_code}\t {code}\t {return_desc}\t {process_time}\t {logRT}\t {guid}\t {userId}\t {requestId}\t header-{header}\t {param_input}\t {respData}\t {msg}\t """
        all_info.info(str(info_msg))
    except Exception as e:
        error_logger.error('access log error :{}'.format(str(e)))


async def get_error_log(request, status_code, code, msg, module_line="-"):
    # acc_logger, server_logger, error_logger, all_info = create_loggers(default_config)
    try:
        t1 = time.time()
        request_header = get_header(request)
        guid = request_header.get('X-GUID') if request_header.get('X-GUID') else "-"
        requestId = TraceID.get_trace() if TraceID.get_trace() else "-"
        userId = request_header.get('X-User-ID') if request_header.get('X-User-ID') else "-"
        header = {"user_ip": get_ip(request), "host": request_header['host'], 'user_id': userId}
        module_line = str(module_line).replace('...', '')
        logRT = get_process_time(t1, time.time())
        info_msg = f'{module_line}\t {status_code}\t {code}\t {logRT}\t {guid}\t {userId}\t {requestId}\t header-{header}\n{msg}'
        error_logger.error(str(info_msg))
    except Exception as e:
        error_logger.error('access log error :{}'.format(str(e)))
        raise e


async def get_service_log_str(method, process_time, log_time_start, status_code, code, return_desc, msg, reqParam,
                              reData):
    # acc_logger, server_logger, error_logger, all_info = create_loggers(default_config)
    try:
        msg = clean_error_message(msg)
        logRT = get_process_time(log_time_start, time.time())
        service_msg = f"""{method}\t {status_code}\t {code}\t {return_desc}\t {process_time}\t {logRT}\t {reqParam}\t {reData} {msg}"""
        server_logger.debug(str(service_msg))
    except Exception as e:
        error_logger.error('service log error :{}'.format(str(e)))
