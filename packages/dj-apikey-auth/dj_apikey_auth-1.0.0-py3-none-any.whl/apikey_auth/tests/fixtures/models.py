import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from apikey_auth.models import APIKey
from apikey_auth.settings.conf import config

User = get_user_model()


@pytest.fixture
def apikey(db, user) -> APIKey:
    """
    Fixture to create an APIKey instance linked to a User.

    Creates an associated APIKey with default settings from
    the config module. The API key is active, unexpired, and has rate limiting
    parameters set based on the configuration.

    Args:
        db: Pytest fixture to enable database access.
        user: The user fixture that used to assign APIKey to it.

    Returns:
        APIKey: The created APIKey instance linked to a User.
    """

    # Create an APIKey instance linked to the user
    apikey = APIKey.objects.create(
        user=user,
        is_active=True,
        requests_count=0,
        max_requests=config.max_requests if hasattr(config, "max_requests") else 1000,
        reset_at=(
            timezone.now() + timezone.timedelta(days=1)
            if getattr(config, "reset_requests_interval", None)
            else None
        ),
    )

    return apikey


@pytest.fixture
def apikey_no_user(db) -> APIKey:
    """
    Fixture to create an APIKey instance not linked to a User.

    Creates an APIKey with no associated user, useful for testing anonymous API key
    authentication scenarios.

    Args:
        db: Pytest fixture to enable database access.

    Returns:
        APIKey: The created APIKey instance with no linked User.
    """
    api_key = APIKey.objects.create(
        user=None,
        is_active=True,
        requests_count=0,
        max_requests=config.max_requests if hasattr(config, "max_requests") else 1000,
        reset_at=(
            timezone.now() + timezone.timedelta(days=1)
            if getattr(config, "reset_requests_interval", None)
            else None
        ),
    )

    return api_key
