from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Category, Content


User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class CategorySerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

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


class UpdateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "name",
            "description",
        ]


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
        ]


class ContentSerializer(serializers.ModelSerializer):
    categories = SimpleCategorySerializer(many=True)
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Content
        fields = [
            "id",
            "title",
            "description",
            "video",
            "categories",
            "user",
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
