"""
@Author  ：duomei
@File    ：test_app.py
@Time    ：2025/3/14 9:39
"""

import os
import pytest
from starlette.testclient import TestClient

from app.app_server.app_view import app
from sthg_fastapi_logs.utils.exception_utils import CustomException

headers = {
    "Authorization": os.getenv("Authorization",
                               "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOjI1MCwicm5TdHIiOiJtV24yekhEemk3bER6SlNKVVZ6RGVDeFlhRTc1YWUyTiIsIm5hbWUiOiJsanEiLCJwYXN0VGltZSI6IjIwMjQtMTEtMjYgMTY6MjA6NTQifQ.3Tv3AP0Mkaa58kl7xE1-e-Fnbnt4RpBYLTYTT5Dv8Xk"),
    "Satoken": os.getenv("Satoken",
                         "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOjI1MCwicm5TdHIiOiJtV24yekhEemk3bER6SlNKVVZ6RGVDeFlhRTc1YWUyTiIsIm5hbWUiOiJsanEiLCJwYXN0VGltZSI6IjIwMjQtMTEtMjYgMTY6MjA6NTQifQ.3Tv3AP0Mkaa58kl7xE1-e-Fnbnt4RpBYLTYTT5Dv8Xk"),
    "Custom-Header": os.getenv("Custom-Header", "custom_value")
}



@pytest.fixture
def client():
    """
    定义一个 pytest fixture 用于提供 TestClient 实例
    """
    return TestClient(app)



# 接口内部异常
#
def test_error_ValueError(client):
    """
    测试获取全部数据源类型接口
    """
    params = {
        "nihao":"你好",
        "shijie":"世界"
    }
    try:
        # 发起 post 请求
        response = client.get(
            "/error_ValueError",
            headers=headers,
            params=params
        )

        # 验证响应状态码
        assert response.status_code == 405
    except  ValueError as e:
        assert '这是一个错误' in str(e)

def test_error_ValueError1(client):
    """
    测试获取全部数据源类型接口
    """
    # params = {
    #     "nihao":"你好",
    #     "shijie":"世界"
    # }
    try:
        # 发起 post 请求
        response = client.get(
            "/error_ValueError",
            headers=headers,
            # params=params
        )

        # 验证响应状态码
        assert response.status_code == 405
    except  ValueError as e:
        assert '这是一个错误' in str(e)


def test_reponse_is_dict(client):
    """
    测试获取全部数据源类型接口
    """
    params = {
        "nihao":"你好",
        "shijie":"世界"
    }
    try:
        # 发起 post 请求
        response = client.get(
            "/reponse_is_dict",
            headers=headers,
            params=params
        )

        # 验证响应状态码
        assert response.status_code == 405
    except Exception as e:
        print(e)


# http请求异常

def test_error_HTTPException(client):
    """
    测试获取全部数据源类型接口
    """
    # params = {
    #     "nihao":"你好",
    #     "shijie":"世界"
    # }
    try:
        # 发起 post 请求
        response = client.get(
            "/error_HTTPException",
            headers=headers,
            # params=params
        )

        # 验证响应状态码
        assert response.status_code == 500
    except  ValueError as e:
        assert '出错了aaaa' in str(e)
    except Exception as e:
        print(e)
#返回空  返回值格式非标准
def test_not_reponse(client):
    """
    测试获取全部数据源类型接口
    """
    # params = {
    #     "nihao":"你好",
    #     "shijie":"世界"
    # }
    try:
        # 发起 post 请求
        response = client.get(
            "/not_reponse",
            headers=headers,
            # params=params
        )

        # 验证响应状态码
        assert response.status_code == 403
    except CustomException as e:
        assert "返回结构不是标准结构" in str(e)
    except  ValueError as e:
        print(e)
# 返回正常
def test_reponse_is_list(client):
    """
    测试获取全部数据源类型接口
    """
    # params = {
    #     "nihao":"你好",
    #     "shijie":"世界"
    # }
    try:
        # 发起 post 请求
        response = client.get(
            "/reponse_is_list",
            headers=headers,
            # params=params
        )

        # 验证响应状态码
        new_response = response.json()
        assert response.status_code == 200
        assert new_response['message'] == '获取规则执行记录 成功'
    except Exception as e:
        print(e)
#

# post 请求body存在 与 不存在
def test_testcdm3(client):
    """
    测试获取全部数据源类型接口
    """
    json_data = {
        "question": "World"
    }
    try:
        # 发起 post 请求
        response = client.post(
            "/testcdm",
            headers=headers,
            json=json_data
        )

        # 验证响应状态码
        new_response = response.json()
        assert new_response.status_code == 200
    except CustomException as e:
        assert "返回结构不是标准结构" in str(e)
    except Exception as e:
        assert "missing 1 required positional argument" in str(e)
#
def test_testcdm1(client):
    """
    测试获取全部数据源类型接口
    """
    json_data = {
        "question": "World"
    }
    try:
        # 发起 post 请求
        response = client.post(
            "/testcdm",
            headers=headers
        )

        # 验证响应状态码
        new_response = response.json()
        assert response.status_code == 403
    except Exception as e:
        print(e)

# 请求接口中的service 异常，传参异常
#
def test_testservice(client):
    """
    测试获取全部数据源类型接口
    """
    json_data = {
        "question": "World"
    }
    try:
        # 发起 post 请求
        response = client.post(
            "/testservice",
            headers=headers,
            json=json_data
        )

        # 验证响应状态码
        new_response = response.json()
        assert response.status_code == 200
    except CustomException as e:
        assert "返回结构不是标准结构" in str(e)
    except Exception as e:
        assert "返回结构不是标准结构" in str(e)

def test_testservice1(client):
    """
    测试获取全部数据源类型接口
    """
    json_data = {
        "question": "World"
    }
    try:
        # 发起 post 请求
        response = client.post(
            "/testservice1",
            headers=headers,
            json=json_data
        )

        # 验证响应状态码
        new_response = response.json()
        assert response.status_code == 200
    except CustomException as e:
        assert "返回结构不是标准结构" in str(e)
    except Exception as e:
        assert 'missing 1 required positional argument' in str(e)