from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/upload_file/", consumers.FileUploadConsumer.as_asgi()),
]
