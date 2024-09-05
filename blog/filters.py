from django_filters import FilterSet
from .models import Content, Category


class ContentFilter(FilterSet):
    class Meta:
        model = Content
        fields = ["categories"]


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = ["user"]
