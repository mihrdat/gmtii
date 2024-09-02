from rest_framework.viewsets import ModelViewSet

from .models import Category, Content
from .serializers import CategorySerializer, ContentSerializer
from .pagination import DefaultLimitOffsetPagination


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = DefaultLimitOffsetPagination


class ContentViewSet(ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    pagination_class = DefaultLimitOffsetPagination
