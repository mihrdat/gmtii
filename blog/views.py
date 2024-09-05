from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)

from .models import Category, Content
from .serializers import (
    CategorySerializer,
    ContentSerializer,
    UpdateContentSerializer,
    UpdateCategorySerializer,
)
from .pagination import DefaultLimitOffsetPagination
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly


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
