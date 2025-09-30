# 代码生成时间: 2025-10-01 03:47:26
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json as sanic_json
import math

# 创建Sanic应用实例
def create_math_calculator():
    app = Sanic('math_calculator')
    
    @app.route('/api/add', methods=['POST'])
    async def add(request: Request):
        """
        实现加法运算
        请求参数应该是一个包含两个数字的列表
        """
        try:
            data = request.json
            if len(data) != 2 or not all(isinstance(x, (int, float)) for x in data):
                return response.json({'error': 'Invalid input'}, status=400)
            result = sum(data)
            return sanic_json({'result': result})
        except Exception as e:
            return response.json({'error': str(e)}, status=500)
    
    @app.route('/api/subtract', methods=['POST'])
    async def subtract(request: Request):
        """
        实现减法运算
        请求参数应该是一个包含两个数字的列表
        """
        try:
            data = request.json
            if len(data) != 2 or not all(isinstance(x, (int, float)) for x in data):
                return response.json({'error': 'Invalid input'}, status=400)
            result = data[0] - data[1]
            return sanic_json({'result': result})
        except Exception as e:
            return response.json({'error': str(e)}, status=500)
    
    @app.route('/api/multiply', methods=['POST'])
    async def multiply(request: Request):
        """
        实现乘法运算
        请求参数应该是一个包含两个数字的列表
        """
        try:
            data = request.json
            if len(data) != 2 or not all(isinstance(x, (int, float)) for x in data):
                return response.json({'error': 'Invalid input'}, status=400)
            result = data[0] * data[1]
            return sanic_json({'result': result})
        except Exception as e:
            return response.json({'error': str(e)}, status=500)
    
    @app.route('/api/divide', methods=['POST'])
    async def divide(request: Request):
        """
        实现除法运算
        请求参数应该是一个包含两个数字的列表，第二个数字不能为0
        """
        try:
            data = request.json
            if len(data) != 2 or not all(isinstance(x, (int, float)) for x in data):
                return response.json({'error': 'Invalid input'}, status=400)
            if data[1] == 0:
                return response.json({'error': 'Cannot divide by zero'}, status=400)
            result = data[0] / data[1]
            return sanic_json({'result': result})
        except Exception as e:
            return response.json({'error': str(e)}, status=500)
    
    return app

if __name__ == '__main__':
    app = create_math_calculator()
    app.run(host='0.0.0.0', port=8000, debug=True)