import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from model_bakery import baker

from blog.models import Category

User = get_user_model()


@pytest.fixture
def create_category(api_client):
    def do_create_category(payload):
        url = reverse("category-list")
        return api_client.post(url, payload)

    return do_create_category


@pytest.fixture
def retrieve_category(api_client):
    def do_retrieve_category(category_id):
        url = reverse("category-detail", kwargs={"pk": category_id})
        return api_client.get(url)

    return do_retrieve_category


@pytest.fixture
def delete_category(api_client):
    def do_delete_category(category_id):
        url = reverse("category-detail", kwargs={"pk": category_id})
        return api_client.delete(url)

    return do_delete_category


@pytest.mark.django_db
class TestCreateCategory:
    def test_if_user_is_anonymous_returns_401(self, create_category):
        user = baker.make(User)
        payload = {"name": "abc", "description": "abc", "user": user.pk}

        response = create_category(payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_category):
        user = baker.make(User)
        payload = {"name": "abc", "description": "abc", "user": user.pk}

        response = create_category(payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_category):
        user = baker.make(User)
        authenticate(user)
        payload = {}

        response = create_category(payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["name"] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_category):
        user = baker.make(User, is_staff=True)
        authenticate(user)
        payload = {"name": "abc", "description": "abc", "user": user.pk}

        response = create_category(payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@pytest.mark.django_db
class TestRetrieveCategory:
    def test_if_category_does_not_exist_returns_404(self, retrieve_category):
        response = retrieve_category(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_category_exists_returns_200(self, retrieve_category):
        category = baker.make(Category)

        response = retrieve_category(category.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("id") == category.id
        assert response.data.get("name") == category.name


@pytest.mark.django_db
class TestDeleteCategory:
    def test_if_user_is_anonymous_returns_401(self, delete_category):
        category = baker.make(Category)

        response = delete_category(category.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, delete_category):
        user = baker.make(User)
        authenticate(user)
        category = baker.make(Category)

        response = delete_category(category.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_category_does_not_exist_returns_404(self, authenticate, delete_category):
        user = baker.make(User, is_staff=True)
        authenticate(user)

        response = delete_category(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_category_exists_returns_204(self, authenticate, delete_category):
        user = baker.make(User, is_staff=True)
        authenticate(user)
        category = baker.make(Category, user=user)

        response = delete_category(category.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Category.objects.filter(id=category.id).exists()
