# 代码生成时间: 2025-09-23 13:08:09
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError, ServerErrorMiddleware
from sanic.response import json
from alembic.config import Config as AlembicConfig
from alembic import command
from alembic.util import CommandError
import sys

# 定义Sanic应用
app = Sanic("DatabaseMigrationTool")

# 定义Alembic配置路径
ALEMBIC_CONFIG = 'alembic.ini'

# 错误处理中间件
@app.exception(ServerError, CommandError)
async def handle_exception(request, exception):
    return response.json(
        {
            "error": str(exception)
        },
        status=500
    )

# 异步运行Alembic命令
async def run_alembic_command(command_name, config=ALEMBIC_CONFIG):
    config = AlembicConfig(config)
    try:
        getattr(command, command_name)(config, sys.argv[1:])
    except CommandError as e:
        raise ServerError(e)

# 定义迁移数据库端点
@app.route('/migrate/<command>', methods=['POST'])
async def migrate(request, command):
    """处理数据库迁移请求"""
    if command not in ['upgrade', 'downgrade', 'stamp']:
        return response.json(
            {
                "error": "Invalid migration command."
            },
            status=400
        )
    try:
        await run_alembic_command(command)
        return response.json(
            {
                "message": f"Migration '{command}' successful."
            }
        )
    except ServerError as e:
        return handle_exception(request, e)

# 启动Sanic服务
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, auto_reload=False, workers=1)
