from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)

from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Content, Publisher
from .serializers import (
    CategorySerializer,
    ContentSerializer,
    UpdateContentSerializer,
    UpdateCategorySerializer,
    PublisherSerializer,
    SimpleCategorySerializer,
)
from .pagination import DefaultLimitOffsetPagination
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .filters import ContentFilter, CategoryFilter

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


class CategoryViewSet(ModelViewSet):
    queryset = (
        Category.objects.prefetch_related("contents").select_related("user").all()
    )
    serializer_class = SimpleCategorySerializer
    pagination_class = DefaultLimitOffsetPagination
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

    def get_queryset(self):
        if not self.request.user.is_staff:
            self.queryset = self.queryset.filter(user=self.request.user)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "retrieve":
            self.serializer_class = CategorySerializer
        elif self.action in ["partial_update", "update"]:
            self.serializer_class = UpdateCategorySerializer
        return super().get_serializer_class()


class ContentViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Content.objects.select_related("user").all()
    serializer_class = ContentSerializer
    pagination_class = DefaultLimitOffsetPagination
    permission_classes = [IsOwnerOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContentFilter

    def get_serializer_class(self):
        if self.action in ["partial_update", "update"]:
            self.serializer_class = UpdateContentSerializer
        return super().get_serializer_class()
