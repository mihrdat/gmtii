import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from channels.db import database_sync_to_async

User = get_user_model()


@database_sync_to_async
def get_user(scope):
    headers = dict(scope["headers"])
    if b"authorization" in headers:
        try:
            (header_type, token) = headers[b"authorization"].decode().split()
            if header_type == "Bearer":
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user = User.objects.get(id=payload["user_id"])
                return user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return AnonymousUser()

    return AnonymousUser()


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope["user"] = await get_user(scope)
        return await self.app(scope, receive, send)
