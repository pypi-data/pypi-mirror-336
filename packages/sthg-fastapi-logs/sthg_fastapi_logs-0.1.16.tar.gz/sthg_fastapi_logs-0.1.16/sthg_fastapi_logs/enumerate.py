from enum import Enum


class CodeEnum(Enum):
    """
    word操作类型
    """
    SUCCESS = "SUCCESS"
    REEOR = "REEOR"
    PARAM_ERROR = "PARAM_ERROR"
    INNER_REEOR = "INNER_REEOR"

class CodeEnum:
    __doc__ = '设置统一的code返回值'
    error = -1  # 查询错误
    success = 0  # 成功
    insufficient_permissions = 1  # 权限不足
    data_duplication = 2  # 数据重复
    repeat_operation = 3  # 重复操作
    data_not_exist = 4  # 数据不存在
    parameter_error = 5  # 参数错误
    space_error = 6  # 空间不足
    state_error = 7  # 状态异常
    connection_data = 8  # 数据存在关联
    task_run = 9  # 任务正在执行
# 定义结果状态枚举
RESULT_SUCCESS = "SUCCESS"
RESULT_ERROR = "ERROR"

class ResultStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

class BusinessCode(Enum):
    OK = "OK"
    INNER_ERROR = "InnerError"
    FORBIDDEN = "Forbidden"
    NOT_FOUND = "NotFound"
    BAD_REQUEST = "BadRequest"

from enum import IntEnum

class HttpStatusCode(IntEnum):
    # 信息性状态码
    CONTINUE = 100
    SWITCHING_PROTOCOLS = 101

    # 成功状态码
    OK = 200
    CREATED = 201
    NO_CONTENT = 204

    # 重定向状态码
    MOVED_PERMANENTLY = 301
    FOUND = 302
    NOT_MODIFIED = 304

    # 客户端错误状态码
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405

    # 服务器错误状态码
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504

    @classmethod
    def get_description(cls, status_code):
        descriptions = {
            cls.CONTINUE: "客户端可以继续发送请求的剩余部分，或者忽略这个响应直接发送请求。",
            cls.SWITCHING_PROTOCOLS: "服务器理解并同意客户端切换协议的请求，后续将使用新协议进行通信。",
            cls.OK: "请求成功，服务器已成功处理请求并返回结果。",
            cls.CREATED: "请求成功，并且服务器已经创建了新的资源。通常在 POST 请求创建资源时使用。",
            cls.NO_CONTENT: "请求成功，但响应中没有返回任何内容。",
            cls.MOVED_PERMANENTLY: "请求的资源已永久移动到新的 URL，后续请求应使用新的 URL。",
            cls.FOUND: "请求的资源临时移动到了新的 URL，客户端应继续使用原 URL 进行后续请求。",
            cls.NOT_MODIFIED: "客户端发送的请求带有缓存验证信息（如 `If-Modified-Since` 或 `If-None-Match`），服务器验证后发现资源未被修改，客户端可以使用本地缓存的版本。",
            cls.BAD_REQUEST: "客户端发送的请求语法错误，不能被服务器所识别。",
            cls.UNAUTHORIZED: "请求需要用户进行身份验证，但客户端未提供有效的身份验证信息。",
            cls.FORBIDDEN: "服务器理解请求客户端的请求，但是拒绝执行此请求。",
            cls.NOT_FOUND: "请求的资源不存在，服务器无法找到对应的资源。",
            cls.METHOD_NOT_ALLOWED: "客户端使用的请求方法（如 GET、POST 等）不被该资源支持。",
            cls.INTERNAL_SERVER_ERROR: "服务器内部发生错误，无法完成请求。",
            cls.BAD_GATEWAY: "服务器作为网关或代理，从上游服务器收到了无效的响应。",
            cls.SERVICE_UNAVAILABLE: "服务器目前无法处理请求，通常是由于服务器过载或正在进行维护。",
            cls.GATEWAY_TIMEOUT: "服务器作为网关或代理，未能及时从上游服务器收到响应。"
        }
        return descriptions.get(status_code, "未知状态码")

class BusinessStatusCode(IntEnum):
    SUCCESS = 2000
    """业务处理成功。"""
    DATA_QUERY_SUCCESS = 2001
    """数据查询成功。"""
    BUSINESS_PARAM_ERROR = 4000
    """业务参数错误，请检查输入。"""
    DATA_ALREADY_EXISTS = 4001
    """数据已存在，请勿重复创建。"""
    BUSINESS_PROCESS_EXCEPTION = 5000
    """业务处理异常，请稍后重试。"""

    @classmethod
    def get_description(cls, code):
        member = cls._member_map_.get(code)
        if member:
            doc = member.__doc__
            return doc if doc else "无描述信息"
        if code == 1:
            return cls.SUCCESS
        if code == 2:
            return ""
        return "未知状态码"