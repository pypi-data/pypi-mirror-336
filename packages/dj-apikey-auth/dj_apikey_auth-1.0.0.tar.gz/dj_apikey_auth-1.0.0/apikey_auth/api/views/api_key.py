from rest_framework import mixins
from rest_framework.permissions import IsAdminUser

from apikey_auth.api.serializers.helper.get_serializer_cls import (
    apikey_serializer_class,
)
from apikey_auth.api.views.base import BaseViewSet
from apikey_auth.models import APIKey


class AdminAPIKeyViewSet(
    BaseViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    """API ViewSet for administrators to manage all API keys.

    Allows staff or superusers to create, update, delete, list, and
    retrieve API keys for any user in the system.

    """

    permission_classes = BaseViewSet.permission_classes + [IsAdminUser]
    serializer_class = apikey_serializer_class()

    def get_queryset(self):
        """Return all API keys for admin management."""
        return APIKey.objects.select_related("user").all()

    def perform_create(self, serializer):
        """Auto-generate API key and enforce user assignment and quota."""
        user = serializer.validated_data.get("user")
        serializer.save(user=user)


class APIKeyViewSet(
    BaseViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    """API ViewSet for users to view their API keys.

    Allows authenticated users to list and retrieve their own API keys.
    Creation, updates, and deletion are restricted to administrators.

    """

    serializer_class = apikey_serializer_class()

    def get_queryset(self):
        """Ensure users can only access their own API keys."""
        return APIKey.objects.select_related("user").filter(user=self.request.user)
