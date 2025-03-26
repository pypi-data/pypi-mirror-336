from rest_framework.permissions import BasePermission

from apikey_auth.models import APIKey


class HasAPIKey(BasePermission):
    """Custom permission to allow access only to requests authenticated with an
    API key.

    This permission checks if the request was authenticated using an API key by verifying
    that `request.auth` is an instance of APIKey, as set by APIKeyAuthentication.

    """

    def has_permission(self, request, view) -> bool:
        """Check if the request is authenticated using an API key.

        Args:
            request(Request): The incoming HTTP request object.
            view(APIView): The view being accessed.

        Returns:
            bool: True if the request.auth is an APIKey instance, False otherwise.

        """
        return hasattr(request, "auth") and isinstance(request.auth, APIKey)
