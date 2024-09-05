from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Category, Content, Publisher


User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class PublisherSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Publisher
        fields = [
            "id",
            "birth_date",
            "user",
            "created_at",
            "updated_at",
        ]


class SimpleContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = [
            "id",
            "title",
            "video",
        ]


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "user",
        ]
        read_only_fields = ["user"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    contents = SimpleContentSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "user",
            "contents",
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


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = [
            "id",
            "title",
            "description",
            "video",
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
