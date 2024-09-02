from rest_framework.viewsets import ModelViewSet

from .models import Category, Video
from .serializers import CategorySerializer, VideoSerializer
from .pagination import DefaultLimitOffsetPagination


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = DefaultLimitOffsetPagination


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    pagination_class = DefaultLimitOffsetPagination
