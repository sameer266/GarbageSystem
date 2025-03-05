# from channels.generic.websocket import AsyncWebsocketConsumer
# from accounts.models import User
# from order.models import Notification
# import json

# class OrderNotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         """Handles WebSocket connection"""
#         user = self.scope['user']
        
#         if user.is_authenticated:
#             self.group_name = f"user_{user.id}"  # Unique group for each user
#             await self.channel_layer.group_add(self.group_name, self.channel_name)
#             await self.accept()
#         else:
#             await self.close()  # Close connection for unauthenticated users

#     async def disconnect(self, close_code):
#         """Handles WebSocket disconnection"""
#         user = self.scope['user']
        
#         if user.is_authenticated:
#             await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def receive(self, text_data):
#         """Handles messages received from the WebSocket"""

#         user = self.scope['user']
#         if user.is_authenticated:
#             # Create a new notification
#             notification = Notification.objects.filter(
#                 user=user,
#                 read=False
#             )

#             # Send the new notification to the user's WebSocket group
#             await self.channel_layer.group_send(
#                 self.group_name,
#                 {
#                     "type": "send_notification",
#                     "message": notification.message,
#                     "order_number": notification.order_number,
#                     "created_at": str(notification.created_at),
#                     "read": notification.read,
#                 }
#             )

#     async def send_notification(self, event):
#         """Handles sending notification to the user"""
#         await self.send(text_data=json.dumps({
#             "message": event["message"],
#             "order_number": event["order_number"],
#             "created_at": event["created_at"],
#             "read": event["read"]
#         }))
