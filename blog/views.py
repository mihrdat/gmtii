from rest_framework.viewsets import ModelViewSet

from .models import Category, Content
from .serializers import CategorySerializer, ContentSerializer
from .pagination import DefaultLimitOffsetPagination
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = DefaultLimitOffsetPagination
    permission_classes = [IsOwnerOrReadOnly, IsAdminOrReadOnly]


class ContentViewSet(ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    pagination_class = DefaultLimitOffsetPagination
    permission_classes = [IsOwnerOrReadOnly, IsAdminOrReadOnly]
