from django.contrib.auth import get_user_model

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)

from .models import Category, Content, Publisher
from .serializers import (
    CategorySerializer,
    ContentSerializer,
    UpdateContentSerializer,
    UpdateCategorySerializer,
    PublisherSerializer,
)
from .pagination import DefaultLimitOffsetPagination
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

User = get_user_model()


class PublisherViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    pagination_class = DefaultLimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(methods=["GET"], detail=True, serializer_class=ContentSerializer)
    def contents(self, request, *args, **kwargs):
        self.queryset = Content.objects.filter(user=self.get_object().user)
        return self.list(request, *args, **kwargs)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = DefaultLimitOffsetPagination
    permission_classes = [IsOwnerOrReadOnly, IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["partial_update", "update"]:
            self.serializer_class = UpdateCategorySerializer
        return super().get_serializer_class()


class ContentViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    pagination_class = DefaultLimitOffsetPagination
    permission_classes = [IsOwnerOrReadOnly, IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["partial_update", "update"]:
            self.serializer_class = UpdateContentSerializer
        return super().get_serializer_class()
