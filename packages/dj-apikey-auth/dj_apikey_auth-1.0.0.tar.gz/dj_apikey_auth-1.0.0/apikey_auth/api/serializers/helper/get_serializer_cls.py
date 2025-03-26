from typing import Type

from rest_framework.serializers import BaseSerializer

from apikey_auth.api.serializers.user import UserSerializer
from apikey_auth.settings.conf import config


def apikey_serializer_class() -> Type[BaseSerializer]:
    """Get the serializer class for the APIKey model, either from config or the
    default.

    Returns:
        The configured serializer class from settings or the default APIKeySerializer.

    """
    from apikey_auth.api.serializers.api_key import APIKeySerializer

    return config.apikey_serializer_class or APIKeySerializer


def user_serializer_class() -> Type[BaseSerializer]:
    """Get the serializer class for the recipient and seen_by fields, either
    from config or the default."""
    return config.user_serializer_class or UserSerializer
