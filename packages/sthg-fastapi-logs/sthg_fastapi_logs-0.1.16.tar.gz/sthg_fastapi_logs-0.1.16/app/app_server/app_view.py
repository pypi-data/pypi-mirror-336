import traceback

from pydantic.main import BaseModel

from sthg_fastapi_logs.exception import register_log_exception

from sthg_fastapi_logs.log_wrapper import register_log_middleware, init_log_config, access_log, service_log
import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()
config = {
    "is_console": True,
}
init_log_config()
register_log_exception(app)
register_log_middleware(app)

from sthg_fastapi_logs.log_wrapper import class_log


@app.get("/error_ValueError")
@access_log(print_res=True, print_req=True)
async def server1():
    t = Test()
    t.get_user_name(a='222222222222')
    t.get_user_id('s', b='11111')
    raise ValueError("这是一个错误")


@app.get("/error_HTTPException")
@access_log(print_res=True)
async def server2():
    raise HTTPException(status_code=403, detail={'msg': "用户无权限"})


@app.get("/not_reponse")
@access_log(print_res=True)
async def server3():
    t = Test()

    t.get_user_name(a='222222222222')
    t.get_user_id(s="s", b='11111')
    return None


@app.get("/reponse_is_list")
@access_log(print_res=True)
async def server4():
    t = Test()
    t.get_user_name(a='222222222222')
    # t.get_user_id("s",b='11111')
    return {"code": 0, "data": {}, "message": "获取规则执行记录 成功", "total": 0}


class Question(BaseModel):
    question: str


@app.post("/reponse_is_dict")
@access_log(print_res=True)
async def server5(obj: Question):
    t = Test()
    t.get_user_name(a='222222222222')
    t.get_user_id("s", b='11111')

    return {
        "data": 200,
        "code": 0,
        "message": "11111"
    }


@app.post("/testcdm")
@access_log(print_res=True)
async def server6(obj: Question):
    t = Test()
    t.get_user_name(a='222222222222')
    t.get_user_id(b='11111')
    return {"Hello": "World", "id": 1}


@app.post("/testservice")
@access_log(print_res=True)
@service_log()
async def server7(obj: Question):

    return {"code": 0, "data": {}, "message": "成功", "total": 0}


@app.post("/testservice1")
@access_log()
@service_log()
async def server8(obj: Question):
    t = Test()
    t.get_user_name(a='222222222222')
    t.get_user_id("s", b='11111')
    return {"code": 0, "data": {}, "message": "成功", "total": 0}


@class_log
class Test():
    def __init__(self):
        self.a = 123
        pass

    def get_user_name(self, a):
        return a

    def get_user_id(self, s, b):
        return b



class NewTest():
    def __init__(self):
        self.a = 456

    def get_user_a_NewTest(self, a):
        return a

    @service_log()
    def get_user_id_NewTest(self, s, b):
        raise ValueError('出错了aaaa')


if __name__ == '__main__':
    uvicorn.run('app_view:app', port=8030, host='0.0.0.0', proxy_headers=False, debug=True,
                timeout_keep_alive=300)
