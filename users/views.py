from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)

from .pagination import DefaultLimitOffsetPagination

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination

    @action(methods=["GET", "PUT", "PATCH"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_current_user
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)

    def get_current_user(self):
        return self.request.user

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            self.queryset = self.queryset.filter(pk=user.pk)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "me":
            if self.request.method in ["PUT", "PATCH"]:
                self.serializer_class = UserUpdateSerializer
        elif self.action == "create":
            self.serializer_class = UserCreateSerializer
        elif self.action in ["update", "partial_update"]:
            self.serializer_class = UserUpdateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        return super().get_permissions()
