import json

from django.core.files.base import ContentFile
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Content, Category
from .constants import Progress, Messages


class FileUploadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        user = self.scope["user"]
        if not user.is_authenticated:
            self.send_error(Messages.ERROR_UNAUTHENTICATED)
            return

        self.metadata = {}
        self.uploaded_file = None
        self.total_size = 0
        self.received_size = 0

    async def receive(self, text_data=None, bytes_data=None):
        try:
            if text_data:
                await self.handle_text_data(text_data)
            elif bytes_data:
                await self.handle_bytes_data(bytes_data)
        except Exception as e:
            await self.handle_error(e)

    async def handle_text_data(self, text_data):
        data = json.loads(text_data)
        if data.get("action") == Progress.ACTION_RESUME:
            await self.send_progress(Progress.RESUMING, offset=self.received_size)
            return

        self.metadata = {
            "title": data.get("title"),
            "description": data.get("description"),
            "categories": data.get("categories"),
        }
        self.total_size = data.get("total_size", 0)

        if not self.uploaded_file:
            self.uploaded_file = ContentFile(b"", name=data.get("title"))

    async def handle_bytes_data(self, bytes_data):
        self.uploaded_file.write(bytes_data)
        self.received_size += len(bytes_data)
        progress_percentage = (self.received_size / self.total_size) * 100
        await self.send_progress(Progress.RECEIVING, progress_percentage)

        if self.received_size == self.total_size:
            await self.save_content()
            await self.send_progress(Progress.COMPLETED, progress_percentage)

    async def send_progress(self, progress, percentage=0, offset=0):
        detail = {
            "progress": progress,
            "received_size": self.received_size,
            "total_size": self.total_size,
            "percentage": percentage,
            "offset": offset,
        }
        await self.send(text_data=json.dumps(detail))

    async def handle_error(self, error):
        detail = {"progress": Progress.ERROR, "error": str(error)}
        await self.send(text_data=json.dumps(detail))
        await self.close()

    async def save_content(self):
        content = Content.objects.create(
            title=self.metadata["title"],
            description=self.metadata["description"],
            video=self.uploaded_file,
        )
        categories = Category.objects.filter(id__in=self.metadata["categories"])
        content.categories.set(categories)
        content.save()
