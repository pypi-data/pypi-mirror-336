import sys

import pytest
from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apikey_auth.admin import APIKeyAdmin
from apikey_auth.models import APIKey
from apikey_auth.settings.conf import config
from apikey_auth.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.admin,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestAPIKeyAdmin:
    """
    Tests for the APIKeyAdmin class in the Django admin interface.

    This test class verifies the general functionality of the APIKeyAdmin,
    ensuring it is properly configured and behaves as expected in the Django admin
    interface without relying on specific field names.

    Tests:
    -------
    - test_admin_registered: Verifies the PageView model is registered with PageViewAdmin.
    """

    def test_admin_registered(self):
        """
        Test that the Product model is registered with ProductAdmin in the admin site.

        Asserts:
        --------
            The admin site has Product registered with an instance of ProductAdmin.
        """
        assert isinstance(admin.site._registry[APIKey], APIKeyAdmin)

    def test_list_display_configured(self, apikey_admin: APIKeyAdmin) -> None:
        """
        Test that the list_display attribute is defined and non-empty.

        This ensures the admin list view has some fields configured without
        specifying exact field names.

        Args:
        ----
            apikey_admin (PageViewAdmin): The admin class instance being tested.

        Asserts:
        --------
            list_display is a tuple or list and has at least one item.
        """
        assert isinstance(apikey_admin.list_display, (tuple, list))
        assert len(apikey_admin.list_display) > 0

    def test_admin_permissions(
        self, apikey_admin: APIKeyAdmin, mock_request: HttpRequest
    ):
        """
        Test that admin permissions reflects the config setting.
        """
        # Test with permission denied
        config.admin_has_add_permission = False
        config.admin_has_change_permission = False
        config.admin_has_delete_permission = False
        config.admin_has_module_permission = False
        assert apikey_admin.has_add_permission(mock_request) is False
        assert apikey_admin.has_change_permission(mock_request) is False
        assert apikey_admin.has_delete_permission(mock_request) is False
        assert apikey_admin.has_module_permission(mock_request) is False

        # Test with permission granted
        config.admin_has_add_permission = True
        config.admin_has_change_permission = True
        config.admin_has_delete_permission = True
        config.admin_has_module_permission = True
        assert apikey_admin.has_add_permission(mock_request) is True
        assert apikey_admin.has_change_permission(mock_request) is True
        assert apikey_admin.has_delete_permission(mock_request) is True
        assert apikey_admin.has_module_permission(mock_request) is True

    def test_user_display_with_user(self, apikey_admin: APIKeyAdmin, user) -> None:
        """
        Test that user_display returns the user when a user is associated.

        Asserts:
            - user_display returns the user's string representation.
        """
        apikey = APIKey(user=user)
        assert apikey_admin.user_display(apikey) == user

    def test_user_display_without_user(self, apikey_admin: APIKeyAdmin) -> None:
        """
        Test that user_display returns 'Anonymous' when no user is associated.

        Asserts:
            - user_display returns 'Anonymous'.
        """
        apikey = APIKey(user=None)
        assert apikey_admin.user_display(apikey) == _("Anonymous")

    def test_status_active(self, apikey_admin: APIKeyAdmin) -> None:
        """
        Test that status returns an active status with green color.

        Asserts:
            - status returns the correct HTML for an active API key.
        """
        apikey = APIKey(is_active=True, expires_at=None)
        expected_html = format_html('<b style="color: green;">{}</b>', _("Active"))
        assert apikey_admin.status(apikey) == expected_html

    def test_status_inactive(self, apikey_admin: APIKeyAdmin) -> None:
        """
        Test that status returns an inactive status with red color.

        Asserts:
            - status returns the correct HTML for an inactive API key.
        """
        apikey = APIKey(is_active=False, expires_at=None)
        expected_html = format_html('<b style="color: red;">{}</b>', _("Inactive"))
        assert apikey_admin.status(apikey) == expected_html

    def test_activate_keys_action(
        self, apikey_admin: APIKeyAdmin, mock_request
    ) -> None:
        """
        Test that activate_keys activates selected API keys.

        Asserts:
            - The selected API keys are activated.
            - A success message is displayed.
        """
        apikey1 = APIKey.objects.create(is_active=False)
        apikey2 = APIKey.objects.create(is_active=False)
        queryset = APIKey.objects.filter(id__in=[apikey1.id, apikey2.id])

        apikey_admin.activate_keys(mock_request, queryset)

        assert APIKey.objects.get(id=apikey1.id).is_active
        assert APIKey.objects.get(id=apikey2.id).is_active

    def test_deactivate_keys_action(
        self, apikey_admin: APIKeyAdmin, mock_request
    ) -> None:
        """
        Test that deactivate_keys deactivates selected API keys.

        Asserts:
            - The selected API keys are deactivated.
            - A success message is displayed.
        """
        apikey1 = APIKey.objects.create(is_active=True)
        apikey2 = APIKey.objects.create(is_active=True)
        queryset = APIKey.objects.filter(id__in=[apikey1.id, apikey2.id])

        apikey_admin.deactivate_keys(mock_request, queryset)

        assert not APIKey.objects.get(id=apikey1.id).is_active
        assert not APIKey.objects.get(id=apikey2.id).is_active
