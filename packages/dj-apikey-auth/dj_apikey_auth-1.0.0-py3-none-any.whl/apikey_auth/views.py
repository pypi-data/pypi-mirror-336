from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from apikey_auth.models import APIKey
from apikey_auth.settings.conf import config


class APIKeyListView(ListView):
    """A class-based view to display a list of API keys for the logged-in user.

    This view renders the API keys in a modern template, applying both
    Django's login requirement and additional DRF-style permissions
    configured via settings.

    """

    template_name = "api_keys.html"
    model = APIKey
    context_object_name = "api_keys"
    permission_classes = [config.view_permission_class]
    ordering = config.view_ordering_fields

    def get_queryset(self):
        """Return the queryset of all API keys.

        Returns:
            QuerySet: A queryset of all APIKey objects in the app.

        """
        return APIKey.objects.select_related("user").all()

    def get_permissions(self):
        """Instantiate and return the list of permissions that this view
        requires.

        Filters out None values (e.g., if config.api_extra_permission_class is None).

        Returns:
            List[BasePermission]: A list of instantiated permission objects.

        """
        return [permission() for permission in self.permission_classes if permission]

    def check_permissions(self, request):
        """Check if the request should be permitted.

        Raises PermissionDenied if any permission check fails.

        Args:
            request(Request): The incoming HTTP request object.

        Raises:
            PermissionDenied: If the user lacks permission to access the view.

        """
        for permission in self.get_permissions():
            if not hasattr(
                permission, "has_permission"
            ) or not permission.has_permission(request, self):
                raise PermissionDenied()

    def dispatch(self, request, *args, **kwargs):
        """Handle the request dispatch, applying permission checks before
        proceeding.

        Args:
            request(Request): The incoming HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The rendered response or a redirect if permission is denied.

        """
        self.check_permissions(request)
        return super().dispatch(request, *args, **kwargs)
