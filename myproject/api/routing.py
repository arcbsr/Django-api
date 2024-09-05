from django.urls import path,re_path
from .consumers import ChatConsumer
from .FileUploadConsumer import FileUploadConsumer

websocket_urlpatterns = [
    path('ws/notification/<str:room_name>/', ChatConsumer.as_asgi()),
    path(r'ws/upload/', FileUploadConsumer.as_asgi()),
]