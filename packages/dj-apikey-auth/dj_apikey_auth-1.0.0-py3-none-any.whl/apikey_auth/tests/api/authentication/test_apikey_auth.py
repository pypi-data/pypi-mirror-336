import sys
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed, Throttled
from rest_framework.test import APIRequestFactory

from apikey_auth.api.authentication import APIKeyAuthentication
from apikey_auth.models import APIKey
from apikey_auth.settings.conf import config
from apikey_auth.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.api,
    pytest.mark.api_authentication,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestAPIKeyAuthentication:
    """
    Tests for the APIKeyAuthentication class.

    This test class verifies the behavior of the APIKeyAuthentication class under various
    conditions, including successful authentication, invalid keys, expiration, rate limiting,
    and caching.
    """

    @pytest.fixture
    def auth(self):
        """Fixture to create an instance of APIKeyAuthentication."""
        return APIKeyAuthentication()

    @pytest.fixture
    def request_factory(self):
        """Fixture to provide a DRF request factory."""
        return APIRequestFactory()

    @patch("apikey_auth.models.config")
    def test_authenticate_success_with_user(
        self, mock_config, auth, request_factory, admin_user
    ):
        """
        Test successful authentication with an API key linked to a user.

        Args:
            auth (APIKeyAuthentication): The authentication instance.
            request_factory (APIRequestFactory): Factory for creating test requests.
            admin_user (User): A User instance to create APIKey for it.

        Asserts:
            Returns a tuple with the user and APIKey instance.
            Rate limit headers are set correctly.
        """
        mock_config.max_requests = 1000
        api_key = APIKey.objects.create(
            user=admin_user,
            is_active=True,
            requests_count=0,
            max_requests=config.max_requests or 1000,
            reset_at=(timezone.now() + timezone.timedelta(days=1)),
        )
        header_prefix = getattr(config, "header_type", "Bearer")
        header_value = (
            f"{header_prefix} {api_key.key}" if header_prefix else api_key.key
        )

        request = request_factory.get("/", HTTP_AUTHORIZATION=header_value)
        result = auth.authenticate(request)

        assert isinstance(result, tuple), "Expected a tuple result."
        assert len(result) == 2, "Expected tuple of length 2."
        assert result[0] == api_key.user, "Expected user to match apikey.user."
        assert result[1] == api_key, "Expected APIKey instance in result."
        assert request.META["X-RateLimit-Limit"] == api_key.max_requests
        assert (
            request.META["X-RateLimit-Remaining"]
            == api_key.max_requests - api_key.requests_count
        )

    def test_authenticate_success_no_user(self, auth, request_factory, apikey_no_user):
        """
        Test successful authentication with an API key not linked to a user.

        Args:
            auth (APIKeyAuthentication): The authentication instance.
            request_factory (APIRequestFactory): Factory for creating test requests.
            apikey_no_user (APIKey): An APIKey instance without a linked user.

        Asserts:
            Returns a tuple with None as user and the APIKey instance.
        """
        header_prefix = getattr(config, "header_type", "Bearer")
        header_value = (
            f"{header_prefix} {apikey_no_user.key}"
            if header_prefix
            else apikey_no_user.key
        )

        request = request_factory.get("/", HTTP_AUTHORIZATION=header_value)
        result = auth.authenticate(request)

        assert isinstance(result, tuple), "Expected a tuple result."
        assert len(result) == 2, "Expected tuple of length 2."
        assert result[0] is None, "Expected user to be None."
        assert result[1] == apikey_no_user, "Expected APIKey instance in result."

    @pytest.mark.django_db
    def test_authenticate_no_header(self, auth, request_factory):
        """
        Test authentication when no API key header is provided.

        Args:
            auth (APIKeyAuthentication): The authentication instance.
            request_factory (APIRequestFactory): Factory for creating test requests.

        Asserts:
            Returns None when no header is present.
        """
        request = request_factory.get("/")
        result = auth.authenticate(request)

        assert result is None, "Expected None when no API key header is provided."

    @pytest.mark.django_db
    def test_authenticate_invalid_key(self, auth, request_factory):
        """
        Test authentication with an invalid API key.

        Args:
            auth (APIKeyAuthentication): The authentication instance.
            request_factory (APIRequestFactory): Factory for creating test requests.

        Asserts:
            Raises AuthenticationFailed for an invalid key.
        """
        header_prefix = getattr(config, "header_type", "Bearer")
        header_value = (
            f"{header_prefix} invalid_key" if header_prefix else "invalid_key"
        )

        request = request_factory.get("/", HTTP_AUTHORIZATION=header_value)
        with pytest.raises(AuthenticationFailed) as exc_info:
            auth.authenticate(request)
        assert str(exc_info.value) == "Invalid API Key."

    def test_authenticate_expired_key(self, auth, request_factory, apikey):
        """
        Test authentication with an expired API key.

        Args:
            auth (APIKeyAuthentication): The authentication instance.
            request_factory (APIRequestFactory): Factory for creating test requests.
            apikey (APIKey): An APIKey instance to modify.

        Asserts:
            Raises AuthenticationFailed for an expired key.
        """
        apikey.expires_at = timezone.now() - timezone.timedelta(days=1)
        apikey.save()

        header_prefix = getattr(config, "header_type", "Bearer")
        header_value = f"{header_prefix} {apikey.key}" if header_prefix else apikey.key

        request = request_factory.get("/", HTTP_AUTHORIZATION=header_value)
        with pytest.raises(AuthenticationFailed) as exc_info:
            auth.authenticate(request)
        assert str(exc_info.value) == "API Key has expired."

    def test_authenticate_invalid_prefix(self, auth, request_factory, apikey):
        """
        Test authentication with an incorrect header prefix.

        Args:
            auth (APIKeyAuthentication): The authentication instance.
            request_factory (APIRequestFactory): Factory for creating test requests.
            apikey (APIKey): An APIKey instance.

        Asserts:
            Raises AuthenticationFailed when prefix doesn’t match config.header_type.
        """
        with patch.object(config, "header_type", "Bearer"):
            header_value = f"WrongPrefix {apikey.key}"
            request = request_factory.get("/", HTTP_AUTHORIZATION=header_value)
            with pytest.raises(AuthenticationFailed) as exc_info:
                auth.authenticate(request)
            assert (
                str(exc_info.value)
                == "Invalid API key format. Expected prefix missing."
            )

    @patch("apikey_auth.api.authentication.apikey_authentication.config")
    def test_authenticate_rate_limit_exceeded(
        self, mock_config, auth, request_factory, apikey
    ):
        """
        Test authentication when the API key exceeds its request limit.

        Args:
            mock_config: Mocked config object to set max_requests.
            auth (APIKeyAuthentication): The authentication instance.
            request_factory (APIRequestFactory): Factory for creating test requests.
            apikey (APIKey): An APIKey instance to modify.

        Asserts:
            Raises Throttled when request limit is exceeded.
        """
        mock_config.max_requests = 1
        mock_config.header_type = None
        mock_config.header_name = "Authorization"
        apikey.max_requests = 1
        apikey.requests_count = 1  # Already at limit
        apikey.save()

        header_prefix = getattr(config, "header_type", "Bearer")
        header_value = f"{header_prefix} {apikey.key}" if header_prefix else apikey.key

        request = request_factory.get("/", HTTP_AUTHORIZATION=header_value)
        with pytest.raises(Throttled) as exc_info:
            auth.authenticate(request)
        assert exc_info.value.detail == "Request limit exceeded with this API Key."

    @patch("apikey_auth.api.authentication.apikey_authentication.config")
    def test_authenticate_rate_limit_exceeded_with_reset(
        self, mock_config, auth, request_factory, apikey
    ):
        """
        Test authentication when the API key exceeds its request limit.

        Args:
            mock_config: Mocked config object to set max_requests.
            auth (APIKeyAuthentication): The authentication instance.
            request_factory (APIRequestFactory): Factory for creating test requests.
            apikey (APIKey): An APIKey instance to modify.

        Asserts:
            Raises Throttled when request limit is exceeded.
        """
        mock_config.max_requests = 1
        mock_config.header_type = None
        mock_config.header_name = "Authorization"
        apikey.max_requests = 1
        apikey.requests_count = 1  # Already at limit
        apikey.reset_at = timezone.now() + timedelta(days=1)
        apikey.save()

        header_prefix = getattr(config, "header_type", "Bearer")
        header_value = f"{header_prefix} {apikey.key}" if header_prefix else apikey.key

        request = request_factory.get("/", HTTP_AUTHORIZATION=header_value)
        with pytest.raises(Throttled) as exc_info:
            auth.authenticate(request)
        assert (
            "Request limit exceeded with this API Key. Expected available in"
            in exc_info.value.detail
        )

    @patch("apikey_auth.api.authentication.apikey_authentication.cache")
    @patch("apikey_auth.api.authentication.apikey_authentication.config")
    def test_authenticate_with_caching(
        self, mock_config, mock_cache, auth, request_factory, apikey
    ):
        """
        Test authentication with caching enabled.

        Args:
            mock_config: Mocked config object to enable caching.
            mock_cache: Mocked cache object to simulate cache behavior.
            auth (APIKeyAuthentication): The authentication instance.
            request_factory (APIRequestFactory): Factory for creating test requests.
            apikey (APIKey): An APIKey instance.

        Asserts:
            Uses cache when enabled and sets cache when key is not found.
        """
        mock_config.use_caching = True
        mock_config.header_type = None
        mock_config.header_name = "Authorization"
        mock_config.cache_timeout = 300
        mock_cache.get.return_value = None  # Cache miss

        header_prefix = getattr(config, "header_type", "Bearer")
        header_value = f"{header_prefix} {apikey.key}" if header_prefix else apikey.key

        request = request_factory.get("/", HTTP_AUTHORIZATION=header_value)
        result = auth.authenticate(request)

        assert result[1] == apikey, "Expected APIKey instance from DB on cache miss."
        mock_cache.get.assert_called_once_with(f"api_key_{apikey.key}")
        mock_cache.set.assert_called_once_with(
            f"api_key_{apikey.key}", apikey, timeout=300
        )

    @patch("apikey_auth.api.authentication.apikey_authentication.cache")
    @patch("apikey_auth.api.authentication.apikey_authentication.config")
    def test_authenticate_cache_hit(
        self, mock_config, mock_cache, auth, request_factory, apikey
    ):
        """
        Test authentication with a cache hit.

        Args:
            mock_config: Mocked config object to enable caching.
            mock_cache: Mocked cache object to simulate cache hit.
            auth (APIKeyAuthentication): The authentication instance.
            request_factory (APIRequestFactory): Factory for creating test requests.
            apikey (APIKey): An APIKey instance.

        Asserts:
            Returns cached APIKey instance without DB query.
        """
        mock_config.use_caching = True
        mock_config.header_type = None
        mock_config.header_name = "Authorization"
        mock_cache.get.return_value = apikey  # Cache hit

        header_prefix = getattr(config, "header_type", "Bearer")
        header_value = f"{header_prefix} {apikey.key}" if header_prefix else apikey.key

        request = request_factory.get("/", HTTP_AUTHORIZATION=header_value)
        result = auth.authenticate(request)

        assert result[1] == apikey, "Expected cached APIKey instance."
        mock_cache.get.assert_called_once_with(f"api_key_{apikey.key}")
