import pytest
from rest_framework.test import APIClient

from apikey_auth.views import APIKeyListView


@pytest.fixture
def api_client() -> APIClient:
    """
    Fixture to initialize the Django REST Framework APIClient for testing.

    :return: An instance of APIClient to make HTTP requests in tests.
    """
    return APIClient()


@pytest.fixture
def view():
    """Fixture to provide an instance of APIKeyListView as a callable view."""
    return APIKeyListView.as_view()


@pytest.fixture
def url():
    """Fixture to provide the URL for the view."""
    return "/api_keys/"
