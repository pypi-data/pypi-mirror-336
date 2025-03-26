"""
@Author  ：duomei
@File    ：code_utils.py
@Time    ：2025/3/11 13:48
"""
import inspect
import os
import re
import traceback

from sthg_fastapi_logs.log_util import get_main_tracebak


def exception_module_func(request,exc,project_folder):
    moduler_func_line = '_'
    route = request.scope.get("route")
    project_root = ""
    main_error = "-"
    method_name = "_"
    if route:
        endpoint = route.endpoint
        # 获取函数的定义信息
        method_name = endpoint.__name__
        module_file = inspect.getmodule(endpoint).__file__
        _,line = inspect.getsourcelines(endpoint)

        # 获取模块对应的文件路径
        project_root = os.path.dirname(os.path.abspath(module_file))
        relative_path = os.path.relpath(module_file, project_root)
        module_path = relative_path.replace(os.sep, '.')[:-3]  # 去除 .py 扩展名
        moduler_func_line = "{}.{}".format(module_path.replace('...',''), method_name)
    else:
        raise Exception('路由未找到')
    if project_root:
            exc_type = type(exc)
            exc_value = exc
            exc_tb = exc.__traceback__
            # 调用 format_exception 函数格式化异常信息
            formatted_exception = traceback.format_exception(exc_type, exc_value, exc_tb)
            # project_path = os.path.dirname(os.path.abspath(project_root))
            # 打印格式化后的异常信息
            main_error = get_main_tracebak(''.join(formatted_exception), project_path=project_root)

    return moduler_func_line,main_error,method_name,project_root,line



# 假设的判断是否为标准结构体的函数
def is_standard_structure(response):
    """
    判断结果是否为标准结构体
    :param response: 方法返回的结果
    :return: True 表示是标准结构体，False 表示不是
    """
    # 这里简单假设标准结构体是字典且包含 'status' 和 'business_code' 字段
    if isinstance(response, dict):
        # 假设标准结构体必须包含 'code' 和'message' 键
        if 'code' in response or 'http_code' in response:
            return True
    return False


# 假设的获取 HTTP 状态码的函数
def get_http_status_code(response):
    """
    从结果中获取 HTTP 状态码
    :param response: 方法返回的结果
    :return: HTTP 状态码，如果不存在则返回 None
    """
    return response.get('http_status_code') if isinstance(response, dict) else None


def get_main_traceback(stack_trace):
    # 定义正则表达式模式，匹配最后一个 raise 语句及相关文件行信息
    pattern = r'File "(.*?)", line (\d+), in (.*?)\s+raise (.*)'
    matches = re.findall(pattern, stack_trace)

    if matches:
        # 取最后一个匹配结果
        file_path, line_number, function_name, raise_statement = matches[-1]
        main_error = f'Traceback (most recent call last):\n File\t"{file_path}",\tline{line_number},\tin\t{function_name}\traise\t{raise_statement}'
    else:
        main_error = "-"
    return main_error


class StandardResult:
    def __init__(self, code, data, message):
        self.code = code
        self.data = data
        self.message = message


# 处理方法结果状态
def handle_method_status(code):
    if isinstance(code, int):
        if 200 <= code < 300:
            return "SUCCESS"
        elif 300 <= code < 400:
            return "REDIRECTION"
        elif code == 400:
            return "BAD_REQUEST"
        elif code == 401:
            return "UNAUTHORIZED"
        elif code == 403:
            return "FORBIDDEN"
        elif code == 404:
            return "NOT_FOUND"
        elif code == 405:
            return "ERROR"
        elif code >= 500:
            return "ERROR"
        elif code == 0:
            return "SUCCESS"
        elif code == 1:
            return "ERROR"
    elif isinstance(code, str):
        return code
    else:
        return "ERROR"


# 处理业务编码
def handle_business_code(code):
    if isinstance(code, int):
        if 200 <= code < 300:
            return "OK"
        elif 300 <= code < 400:
            return "Redirection"
        elif code == 400:
            return "BadRequest"
        elif code == 401:
            return "Unauthorized"
        elif code == 403:
            return "Forbidden"
        elif code == 404:
            return "NotFound"
        elif code == 405:
            return "InnerError"
        elif code >= 500:
            return "InnerError"
        elif code == 0:
            return "OK"
        elif code == 1:
            return "InnerError"
    elif isinstance(code, str):
        return code
    else:
        return "ERROR"
