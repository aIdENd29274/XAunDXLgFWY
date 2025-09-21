# 代码生成时间: 2025-09-21 12:52:56
from sanic import Sanic, response
from sanic.exceptions import ServerError, ServerErrorMiddleware
from sanic.log import logger
from sanic.request import Request
from sanic.response import json

# Define a simple data structure for a notification
class Notification:
    def __init__(self, message, recipient):
        self.message = message
        self.recipient = recipient

# Notification service class
class NotificationService:
    def __init__(self):
        self.notifications = []

    def send_notification(self, notification):
        # Simulate sending a notification
        self.notifications.append(notification)
        return True, "Notification sent successfully."

    def get_all_notifications(self):
        return self.notifications

# Initialize the notification service
notification_service = NotificationService()

# Initialize the Sanic application
app = Sanic("MessageNotificationSystem")

# Error handler for Sanic
@app.exception(ServerError)
async def server_error(request, exception):
    logger.error(f"ServerError: {exception}")
    return json({
        "error": "Internal Server Error",
        "message": str(exception)
    }), 500

# Endpoint to send a notification
@app.route("/send", methods=["POST"])
async def send_notification(request: Request):
    try:
        data = request.json
        notification = Notification(data.get("message"), data.get("recipient"))
        success, message = notification_service.send_notification(notification)
        if success:
            return response.json({
                "status": "success",
                "message": message
            }, 200)
        else:
            raise ServerError("Failed to send notification.")
    except KeyError as e:
        raise ServerError(f"Missing data: {e}")
    except Exception as e:
        raise ServerError(f"An error occurred: {e}")

# Endpoint to retrieve all notifications
@app.route("/notifications", methods=["GET"])
async def get_notifications(request: Request):
    try:
        notifications = notification_service.get_all_notifications()
        return response.json([
            {
                "message": n.message,
                "recipient": n.recipient
            } for n in notifications
        ], 200)
    except Exception as e:
        raise ServerError(f"An error occurred: {e}")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, auto_reload=False, debug=True)