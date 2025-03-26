import pytest
from django.contrib.admin import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpRequest
from django.test import RequestFactory

from apikey_auth.admin import APIKeyAdmin
from apikey_auth.models import APIKey


@pytest.fixture
def request_factory() -> RequestFactory:
    """
    Fixture to provide an instance of RequestFactory.

    Returns:
    -------
        RequestFactory: An instance of Django's RequestFactory.
    """
    return RequestFactory()


@pytest.fixture
def mock_request():
    """
    Fixture to provide a mock HttpRequest object with messages support.

    Returns:
        HttpRequest: A Django HttpRequest object with messages middleware support.
    """
    request = RequestFactory().get('/')
    setattr(request, 'session', 'session')
    messages_storage = FallbackStorage(request)
    setattr(request, '_messages', messages_storage)
    return request


@pytest.fixture
def admin_site() -> AdminSite:
    """
    Fixture to provide an instance of AdminSite.

    Returns:
    -------
        AdminSite: An instance of Django's AdminSite.
    """
    return AdminSite()


@pytest.fixture
def apikey_admin(admin_site: AdminSite) -> APIKeyAdmin:
    """
    Fixture to provide an instance of APIKeyAdmin.

    Args:
    ----
        admin_site (AdminSite): An instance of Django's AdminSite.

    Returns:
    -------
        PageViewAdmin: An instance of APIKeyAdmin.
    """
    return APIKeyAdmin(APIKey, admin_site)
