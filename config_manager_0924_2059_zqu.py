# 代码生成时间: 2025-09-24 20:59:01
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError, ConfigError
from sanic.config import Config as SanicConfig
from sanic.log import logger
from sanic.exceptions import ServerError

# 配置文件管理器
class ConfigManager:
    def __init__(self, app, config_file):
        """初始化配置文件管理器
        :param app: Sanic应用
        :param config_file: 配置文件路径
        """
        self.app = app
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        """加载配置文件
        """
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.app.config.update(config)
        except FileNotFoundError:
            logger.error(f"配置文件 {self.config_file} 不存在")
            raise ServerError("配置文件不存在")
        except json.JSONDecodeError:
            logger.error(f"配置文件 {self.config_file} 格式错误")
            raise ServerError("配置文件格式错误")

    def get_config(self, key):
        """获取配置项
        :param key: 配置项键
        :return: 配置项值
        """
        return self.app.config.get(key)

    def set_config(self, key, value):
        """设置配置项
        :param key: 配置项键
        :param value: 配置项值
        """
        self.app.config[key] = value


# Sanic应用
app = Sanic(__name__)

# 配置文件路径
config_file = 'config.json'

# 创建配置文件管理器实例
config_manager = ConfigManager(app, config_file)

# 获取配置项
@app.route('/get_config/<key>', methods=['GET'])
async def get_config(request, key):
    """获取配置项"""
    try:
        value = config_manager.get_config(key)
        if value is None:
            return response.json({'error': f'配置项 {key} 不存在'})
        return response.json({'value': value})
    except ServerError as e:
        return response.json({'error': str(e)})

# 设置配置项
@app.route('/set_config/<key>', methods=['POST'])
async def set_config(request, key):
    """设置配置项"""
    try:
        value = request.json.get('value')
        if value is None:
            return response.json({'error': '配置项值不能为空'})
        config_manager.set_config(key, value)
        return response.json({'message': '配置项设置成功'})
    except ServerError as e:
        return response.json({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, workers=2)