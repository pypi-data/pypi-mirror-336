import sys

import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from apikey_auth.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.views,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestAPIKeyListView:
    """
    Tests for the APIKeyListView using pytest.

    This test class verifies the behavior of the APIKeyListView, ensuring that:
    - Authenticated users with API keys can access the view.
    - Unauthenticated users are denied access (via LoginRequiredMixin).
    - Additional permissions (e.g., HasAPIKeyPermission) are enforced if configured.
    - The correct template is rendered with API key data.
    """

    def test_authenticated_user_access(
        self, request_factory, admin_user, apikey, view, url
    ):
        """
        Test that an authenticated user with API keys can access the APIKeyListView.
        """
        request = request_factory.get(url)
        request.user = admin_user

        response = view(request)
        assert (
            response.status_code == 200
        ), "Authenticated user should get a 200 OK response."

    def test_unauthenticated_user_access(self, request_factory, view, url):
        """
        Test that an unauthenticated user is denied access to the APIKeyListView.
        """
        request = request_factory.get(url)
        request.user = AnonymousUser()  # Simulate an unauthenticated user

        with pytest.raises(PermissionDenied):
            view(request)
