"""
@Author  ：duomei
@File    ：exception_utils.py
@Time    ：2025/3/11 13:38
"""

# 自定义异常类
class TableNameError(Exception):
    __doc__ = "数据库表名命名规则验证错误"


class ColumnNameError(Exception):
    __doc__ = "数据库表属性命名规则验证错误"


class RepetitiveError(Exception):
    __doc__ = "数据库表字段重复错误"


class DataNotFoundError(Exception):
    __doc__ = "数据库数据未找到"


class ParamLackError(Exception):
    __doc__ = "缺少参数"


class ParamValidatedError(Exception):
    __doc__ = "自定义参数格式不正确"


class AlreadyExistsError(Exception):
    __doc__ = "资源已存在"


class CustomRaiseError(Exception):
    __doc__ = "封装自定义报错"
    """
    使用框架自动捕获异常时候使用
    use:
        raise CustomRaiseError(*e.args, int)
    params:
        *e.args: 原始的错误信息
        int: 想要的业务报错信息code
    """
class CustomException(Exception):
    """
    自定义异常类，继承自 Exception
    """
    def __init__(self, message="自定义异常"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
