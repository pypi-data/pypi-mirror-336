from pydantic import BaseModel, Field
from sanic import Blueprint, Sanic, json
from sanic.log import logger

from sanic_api.api import Request
from sanic_api.app import BaseApp
from sanic_api.config import DefaultSettings

user_blueprint = Blueprint("user", "/user")


class UserInfoModel(BaseModel):
    user_id: int = Field(title="用户ID")


class UserInfoResponse(BaseModel):
    user_name: str = Field(title="用户名")


class UseLoginRequest(Request):
    """
    用户登录
    用户登录描述
    这也是描述
    """

    form_data: UserInfoModel


@user_blueprint.post("info")
async def user_info(request: Request, json_data: UserInfoModel):
    """
    获取用户信息
    """
    logger.info(f"data: {json_data}")
    info = UserInfoResponse(user_name="张三")
    return request.json_resp(info, server_code="0000", server_msg="查询成功")


@user_blueprint.post("login")
async def user_login(request: UseLoginRequest):
    """
    用户登录
    """
    logger.info(f"user_id: {request.form_data.user_id}")
    return json(request.form_data.model_dump())


class App(BaseApp):
    """
    服务示例
    """

    async def setup_route(self, app: Sanic):
        api = Blueprint.group(url_prefix="api")
        api.append(user_blueprint)
        app.blueprint(api)


if __name__ == "__main__":
    settings = DefaultSettings()
    settings.port = 9999
    settings.logger.loki_url = "http://127.0.0.1:23100/loki/api/v1/push"
    App.run(settings)
