import logging
from typing import Optional, Tuple

from django.core.cache import cache
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, Throttled
from rest_framework.request import Request

from apikey_auth.models import APIKey
from apikey_auth.settings.conf import config

logger = logging.getLogger(__name__)


class APIKeyAuthentication(BaseAuthentication):
    """Custom authentication for API key-based access.

    Authenticates requests using an API key from the headers. If the key
    is valid and linked to a user, that user is returned as
    request.user. The APIKey instance is attached to request.api_key for
    additional metadata access.

    """

    def authenticate(
        self, request: Request
    ) -> Optional[Tuple[Optional[object], Optional[APIKey]]]:
        """Authenticate a request using an API key from the request headers.

        Extracts the API key from the configured header (e.g., 'Authorization'),
        validates it against the database, checks expiration and rate limits,
        and returns the associated user (if any) and the APIKey instance.

        Args:
            request: The incoming HTTP request object.

        Returns:
            Tuple[Optional[object], Optional[APIKey]]: A tuple containing the authenticated
                user (or None if no user is linked) and the APIKey instance, per DRF's
                authentication contract. Returns None if no API key is provided.

        Raises:
            AuthenticationFailed: If the API key is invalid or expired.
            Throttled: If the request limit is exceeded, with an optional wait time.

        """
        header_prefix = f"{config.header_type} " if config.header_type else ""
        api_key = request.headers.get(config.header_name.lower(), "")
        if config.header_type and not api_key.startswith(config.header_type):
            raise AuthenticationFailed(
                _("Invalid API key format. Expected prefix missing.")
            )
        api_key = api_key.replace(header_prefix, "")
        if not api_key:
            return None  # No API key present, proceed to other authentication

        # Validate the API key
        try:
            if config.use_caching:
                cache_key = f"api_key_{api_key}"
                api_key_instance = cache.get(cache_key)
                if not api_key_instance:
                    api_key_instance = APIKey.objects.select_related("user").get(
                        key=api_key, is_active=True
                    )
                    cache.set(cache_key, api_key_instance, timeout=config.cache_timeout)
            else:
                api_key_instance = APIKey.objects.select_related("user").get(
                    key=api_key, is_active=True
                )
        except APIKey.DoesNotExist:
            logger.warning("Authentication failed: Invalid API key '%s'", api_key)
            raise AuthenticationFailed(_("Invalid API Key."))

        if api_key_instance.has_expired():
            raise AuthenticationFailed(_("API Key has expired."))

        if config.max_requests and not api_key_instance.increment_requests():
            reset_at = api_key_instance.reset_at
            detail = _("Request limit exceeded with this API Key.")
            if reset_at:
                now = timezone.now()
                seconds_until_reset = max(0, (reset_at - now).total_seconds())
                raise Throttled(wait=seconds_until_reset, detail=force_str(detail))
            raise Throttled(detail=detail)

        if api_key_instance.max_requests is not None:
            request.META["X-RateLimit-Limit"] = api_key_instance.max_requests
            request.META["X-RateLimit-Remaining"] = max(
                0, api_key_instance.max_requests - api_key_instance.requests_count
            )

        # Return the associated user (if any) and the API key as auth token
        return (
            (api_key_instance.user, api_key_instance)
            if api_key_instance.user
            else (None, api_key_instance)
        )
