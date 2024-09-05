from rest_framework import serializers
from .models import Category, Content


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


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = [
            "id",
            "title",
            "description",
            "video",
            "categories",
            "created_at",
            "updated_at",
        ]


class UpdateContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = [
            "title",
            "description",
            "categories",
        ]
