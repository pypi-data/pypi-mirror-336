#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：LiShun
@File    ：exception.py
@Time    ：2022/7/12 18:56
@Desc    ：
"""
# __all__ = [
#     'BaseHTTPException', 'register_exception'
# ]

import os
import time
import traceback
from typing import Any, Optional, Dict

from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError

from .base_code.code import CODE
from sthg_fastapi_logs.utils.code_utils import handle_method_status, handle_business_code, exception_module_func
from .enumerate import  HttpStatusCode
from .log_util import get_main_tracebak
from .log_wrapper import get_error_log, get_service_log_str, get_process_time


def json_response(data=None, message=None, code=200, status_code=200) -> Response:
    code_dict = CODE.get(code) or CODE[400]
    return JSONResponse(
        status_code=status_code,
        content={
            "code": code_dict["code"],
            "message": message or code_dict["zh-cn"],
            "data": data
        }
    )


class BaseHTTPException(HTTPException):
    EXC_STATUS_CODE = 500
    EXC_CODE = 1000
    EXC_MESSAGE = None

    def __init__(
            self,
            message: Any = None,
            status_code: int = 500,
            code: int = 40000,
            headers: Optional[Dict[str, Any]] = None
    ) -> None:
        self.message = message or self.EXC_MESSAGE
        self.status_code = status_code or self.EXC_STATUS_CODE
        self.code = code or self.EXC_CODE
        self.headers = headers

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, message={self.message!r})"


def register_log_exception(app: FastAPI):
    """
    捕获FastApi异常
    :param app:
    :return:
    """
    start_time = time.time()
    async def log_and_response(request, exc, default_code=500, status_code=None):
        msg = traceback.format_exc()
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        project_folder = os.path.dirname(current_file_dir)


        module_line, main_error, method_name, project_root,line = exception_module_func(request, exc,project_folder)
        new_status_code = status_code
        new_code = default_code
        if status_code:
            status_code = handle_method_status(default_code)
        code = handle_business_code(default_code)
        await get_error_log(request, status_code=status_code, code=code, msg=msg, module_line=module_line)


        server_msg = get_main_tracebak(traceback.format_exc(), project_path=project_root)
        if "File" not in server_msg:
            server_msg = "File '{}', line {} in {} {}".format(project_root,line,method_name,server_msg)
        server_msg = "Traceback (most recent call last):\n" + server_msg
        module_line = module_line.replace('...','.')
        process_time = get_process_time(start_time, time.time())
        await get_service_log_str(module_line, process_time=process_time, log_time_start=time.time(),status_code=status_code, code=code,
                            return_desc=HttpStatusCode.get_description(new_status_code), msg=server_msg,
                            reqParam="-",reData='-')
        message = str(exc) if not isinstance(exc, AssertionError) else ''.join(exc.args)
        if isinstance(exc, RequestValidationError):
            message = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
        if isinstance(exc, HTTPException):
            message = str(exc.detail)
        if isinstance(exc, BaseHTTPException):
            message = str(exc.message)
        return json_response(code=default_code, message=message, status_code=new_status_code)

    ####################
    @app.exception_handler(Exception)
    async def exception_handle(request: Request, exc: Exception):
        # 处理所有未捕获的异常
        return await log_and_response(request, exc, default_code=500, status_code=500)

    @app.exception_handler(HTTPException)
    async def http_exception_handle(request: Request, exc: HTTPException):
        # 处理HTTP异常
        return await log_and_response(request, exc, default_code=500, status_code=500)

    @app.exception_handler(BaseHTTPException)
    async def base_http_exception_handle(request: Request, exc: BaseHTTPException):
        # 处理自定义的BaseHTTPException异常
        return await log_and_response(request, exc, default_code=500, status_code=500)

    @app.exception_handler(AssertionError)
    async def assert_exception_handle(request: Request, exc: AssertionError):
        # 处理断言错误
        return await log_and_response(request, exc, default_code=403, status_code=403)

    @app.exception_handler(ValidationError)
    async def validation_exception_handle(request: Request, exc: ValidationError):
        # 处理验证错误
        return await log_and_response(request, exc, default_code=403, status_code=403)

    @app.exception_handler(RequestValidationError)
    async def request_exception_handler(request: Request, exc: RequestValidationError):
        # 处理请求验证错误
        return await log_and_response(request, exc, default_code=403, status_code=403)
