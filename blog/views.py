from rest_framework.viewsets import ModelViewSet

from .models import Category
from .serializers import CategorySerializer
from .pagination import DefaultLimitOffsetPagination


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = DefaultLimitOffsetPagination
