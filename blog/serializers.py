from rest_framework import serializers
from .models import Category, Video


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "user",
            "created_at",
            "updated_at",
        ]


class VideoSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()

    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "description",
            "file",
            "category_id",
            "created_at",
            "updated_at",
        ]
