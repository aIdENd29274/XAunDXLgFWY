# 代码生成时间: 2025-09-18 01:38:14
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import ServerError, Unauthorized
from sanic.log import logger
from sanic.request import Request

# 假设的用户数据库
users_db = {"admin": {"password": "admin123", "roles": ["admin"]}}

app = Sanic("UserLoginSystem")

"""
用户登录端点
路径：/login
方法：POST
参数：username, password
返回：成功时返回用户信息，失败时返回错误信息
"""
@app.route("/login", methods=["POST"])
async def login(request: Request):
    # 获取请求数据
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # 检查参数是否齐全
    if not username or not password:
        raise ServerError("Username and password are required.")

    # 检查用户是否存在
    user = users_db.get(username)
    if not user:
        raise Unauthorized("User not found.")

    # 检查密码是否正确
    if user["password"] != password:
        raise Unauthorized("Incorrect password.")

    # 如果验证成功，返回用户信息
    return json({"message": "Login successful", "user": user})

# 运行Sanic应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)