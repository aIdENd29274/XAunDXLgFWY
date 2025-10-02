# 代码生成时间: 2025-10-03 03:55:39
import psutil
from sanic import Sanic, response

# 创建Sanic应用
app = Sanic('SystemPerformanceMonitor')

# 获取CPU使用率的路由
@app.route('/cpu_usage', methods=['GET'])
def cpu_usage(request):
    # 获取当前CPU使用率
    cpu_usage_percent = psutil.cpu_percent()
    # 返回CPU使用率数据
    return response.json({'cpu_usage': cpu_usage_percent})

# 获取内存使用情况的路由
@app.route('/memory_usage', methods=['GET'])
def memory_usage(request):
    # 获取内存使用情况
    memory = psutil.virtual_memory()
    # 返回内存使用数据
    return response.json({'total': memory.total, 'available': memory.available})

# 获取磁盘使用情况的路由
@app.route('/disk_usage', methods=['GET'])
def disk_usage(request):
    # 获取磁盘使用情况
    disk_usage = psutil.disk_usage('/')
    # 返回磁盘使用数据
    return response.json({'total': disk_usage.total, 'used': disk_usage.used, 'free': disk_usage.free})

# 获取网络使用情况的路由
@app.route('/network_usage', methods=['GET'])
def network_usage(request):
    # 获取网络使用情况
    network_io = psutil.net_io_counters()
    # 返回网络使用数据
    return response.json({'bytes_sent': network_io.bytes_sent, 'bytes_recv': network_io.bytes_recv})

# 运行Sanic应用程序
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
