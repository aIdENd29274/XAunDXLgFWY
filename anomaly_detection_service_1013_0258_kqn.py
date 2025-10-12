# 代码生成时间: 2025-10-13 02:58:32
import sanic
from sanic.response import json
from sanic.exceptions import ServerError, NotFound
import numpy as np
from sklearn.ensemble import IsolationForest

# 定义异常检测服务
class AnomalyDetectionService:
    """Anomaly detection service using Isolation Forest algorithm."""

    def __init__(self, contamination=0.1):
        """
        Args:
            contamination (float): The proportion of outliers in the data set.
        """
        self.contamination = contamination
        self.model = IsolationForest(contamination=contamination)

    def fit(self, X):
        """Train the model with the provided dataset."""
        try:
            self.model.fit(X)
        except Exception as e:
            raise ServerError("Failed to fit the model: {}".format(str(e)))

    def predict(self, X):
        """Predict whether each data point is an outlier."""
        try:
            return self.model.predict(X)
        except Exception as e:
            raise ServerError("Failed to predict anomalies: {}".format(str(e)))

    def score_samples(self, X):
        """Return the anomaly score of each sample."""
        try:
            return self.model.decision_function(X)
        except Exception as e:
            raise ServerError("Failed to score samples: {}".format(str(e)))

# 创建Sanic应用
app = sanic.Sanic('AnomalyDetectionApp')

# 初始化异常检测服务
anomaly_service = AnomalyDetectionService()

# 定义API端点来训练模型
@app.post('/train')
async def train(request):
    """Train the anomaly detection model with the provided dataset."""
    try:
        data = request.json
        X = np.array(data['X'])
        anomaly_service.fit(X)
        return json({'message': 'Model trained successfully'})
    except Exception as e:
        raise ServerError(str(e))

# 定义API端点来预测异常
@app.post('/predict')
async def predict(request):
    """Predict whether each data point in the dataset is an outlier."""
    try:
        data = request.json
        X = np.array(data['X'])
        predictions = anomaly_service.predict(X)
        return json({'predictions': predictions.tolist()})
    except Exception as e:
        raise ServerError(str(e))

# 定义API端点来获取异常分数
@app.post('/score')
async def score(request):
    """Return the anomaly score of each sample in the dataset."""
    try:
        data = request.json
        X = np.array(data['X'])
        scores = anomaly_service.score_samples(X)
        return json({'scores': scores.tolist()})
    except Exception as e:
        raise ServerError(str(e))

# 添加错误处理器
@app.exception(ServerError)
async def handle_server_error(request, exception):
    return json({'error': str(exception)}, status=500)

# 添加未找到处理器
@app.exception(NotFound)
async def handle_not_found(request, exception):
    return json({'error': 'Not Found'}, status=404)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)