from django.contrib.auth.models import User
from rest_framework.test import APIClient
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(user):
        return api_client.force_authenticate(user=user)

    return do_authenticate
