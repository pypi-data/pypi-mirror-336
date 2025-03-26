import sys
from unittest.mock import MagicMock, patch

import pytest

from apikey_auth.settings.checks import check_apikey_settings
from apikey_auth.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.settings,
    pytest.mark.settings_checks,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestAPIKeySettings:
    @patch("apikey_auth.settings.checks.config")
    def test_valid_settings(self, mock_config: MagicMock) -> None:
        """
        Test that valid settings produce no errors.

        Args:
        ----
            mock_config (MagicMock): Mocked configuration object with valid settings.

        Asserts:
        -------
            No errors are returned when all settings are valid.
        """
        # Mock all config values to be valid
        # Admin settings
        mock_config.admin_has_add_permission = True
        mock_config.admin_has_change_permission = False
        mock_config.admin_has_delete_permission = True
        mock_config.admin_has_module_permission = False

        # APIKey
        mock_config.header_name = "Authorization"
        mock_config.header_type = None
        mock_config.use_caching = False
        mock_config.cache_timeout = 200
        mock_config.reset_requests_interval = None
        mock_config.max_requests = None

        # Global API settings
        mock_config.api_allow_list = True
        mock_config.api_allow_retrieve = False
        mock_config.api_allow_create = True
        mock_config.api_allow_update = True
        mock_config.api_allow_delete = True
        mock_config.base_user_throttle_rate = "100/day"
        mock_config.staff_user_throttle_rate = "200/hour"
        mock_config.view_ordering_fields = ["created_at"]

        mock_config.api_ordering_fields = [
            "max_requests",
            "requests_count",
            "created_at",
            "expires_at",
            "max_requests",
            "reset_at",
        ]
        mock_config.api_search_fields = ["id"]

        mock_config.get_setting.side_effect = lambda name, default: default

        errors = check_apikey_settings(None)
        assert not errors, f"Expected no errors for valid settings, but got {errors}"

    @patch("apikey_auth.settings.checks.config")
    def test_invalid_boolean_settings(self, mock_config: MagicMock) -> None:
        """
        Test that invalid boolean settings return errors.

        Args:
        ----
            mock_config (MagicMock): Mocked configuration object with invalid boolean settings.

        Asserts:
        -------
            Errors are returned for invalid boolean values in settings.
        """
        # Set valid defaults for non-boolean settings
        # APIKey
        mock_config.header_name = "Authorization"
        mock_config.header_type = None
        mock_config.cache_timeout = 200
        mock_config.reset_requests_interval = None
        mock_config.max_requests = None

        # Global API settings
        mock_config.base_user_throttle_rate = "100/day"
        mock_config.staff_user_throttle_rate = "200/hour"

        mock_config.view_ordering_fields = ["created_at"]
        mock_config.api_ordering_fields = [
            "max_requests",
            "requests_count",
            "created_at",
            "expires_at",
            "max_requests",
            "reset_at",
        ]
        mock_config.api_search_fields = ["id"]

        mock_config.get_setting.side_effect = lambda name, default: default

        # Invalid boolean settings
        mock_config.admin_has_add_permission = "not_boolean"
        mock_config.admin_has_change_permission = "not_boolean"
        mock_config.admin_has_delete_permission = "not_boolean"
        mock_config.admin_has_module_permission = "not_boolean"
        mock_config.api_allow_list = "not_boolean"
        mock_config.api_allow_retrieve = "not_boolean"
        mock_config.api_allow_create = "not_boolean"
        mock_config.api_allow_update = "not_boolean"
        mock_config.api_allow_delete = "not_boolean"
        mock_config.use_caching = "not_boolean"

        mock_config.get_setting.side_effect = lambda name, default: default

        errors = check_apikey_settings(None)
        assert (
            len(errors) == 10
        ), f"Expected 10 errors for invalid booleans, but got {len(errors)}"
        error_ids = [error.id for error in errors]
        expected_ids = [
            f"apikey_auth.E001_{mock_config.prefix}ADMIN_HAS_ADD_PERMISSION",
            f"apikey_auth.E001_{mock_config.prefix}ADMIN_HAS_CHANGE_PERMISSION",
            f"apikey_auth.E001_{mock_config.prefix}ADMIN_HAS_DELETE_PERMISSION",
            f"apikey_auth.E001_{mock_config.prefix}ADMIN_HAS_MODULE_PERMISSION",
            f"apikey_auth.E001_{mock_config.prefix}API_ALLOW_LIST",
            f"apikey_auth.E001_{mock_config.prefix}API_ALLOW_RETRIEVE",
            f"apikey_auth.E001_{mock_config.prefix}API_ALLOW_CREATE",
            f"apikey_auth.E001_{mock_config.prefix}API_ALLOW_DELETE",
            f"apikey_auth.E001_{mock_config.prefix}API_ALLOW_UPDATE",
            f"apikey_auth.E001_{mock_config.prefix}USE_CACHING",
        ]
        assert all(
            eid in error_ids for eid in expected_ids
        ), f"Expected error IDs {expected_ids}, got {error_ids}"

    @patch("apikey_auth.settings.checks.config")
    def test_invalid_list_settings(self, mock_config: MagicMock) -> None:
        """
        Test that invalid list settings return errors.

        Args:
        ----
            mock_config (MagicMock): Mocked configuration object with invalid list settings.

        Asserts:
        -------
            Errors are returned for invalid list values in settings.
        """
        # Valid boolean and throttle settings
        # Admin settings
        mock_config.admin_has_add_permission = True
        mock_config.admin_has_change_permission = False
        mock_config.admin_has_delete_permission = True
        mock_config.admin_has_module_permission = False

        # APIKey
        mock_config.header_name = "Authorization"
        mock_config.header_type = None
        mock_config.use_caching = False
        mock_config.cache_timeout = 200
        mock_config.reset_requests_interval = None
        mock_config.max_requests = None

        # Global API settings
        mock_config.api_allow_list = True
        mock_config.api_allow_retrieve = False
        mock_config.api_allow_create = True
        mock_config.api_allow_update = True
        mock_config.api_allow_delete = True
        mock_config.base_user_throttle_rate = "100/day"
        mock_config.staff_user_throttle_rate = "200/hour"

        # Invalid list settings
        mock_config.api_ordering_fields = []  # Empty list
        mock_config.api_search_fields = [123]  # Invalid type
        mock_config.view_ordering_fields = []

        mock_config.get_setting.side_effect = lambda name, default: default

        errors = check_apikey_settings(None)
        assert (
            len(errors) == 3
        ), f"Expected 3 errors for invalid lists, but got {len(errors)}"
        error_ids = [error.id for error in errors]
        expected_ids = [
            f"apikey_auth.E003_{mock_config.prefix}VIEW_ORDERING_FIELDS",
            f"apikey_auth.E003_{mock_config.prefix}API_ORDERING_FIELDS",
            f"apikey_auth.E004_{mock_config.prefix}API_SEARCH_FIELDS",
        ]
        assert all(
            eid in error_ids for eid in expected_ids
        ), f"Expected error IDs {expected_ids}, got {error_ids}"

    @patch("apikey_auth.settings.checks.config")
    def test_invalid_throttle_rate(self, mock_config: MagicMock) -> None:
        """
        Test that invalid throttle rates return errors.

        Args:
        ----
            mock_config (MagicMock): Mocked configuration object with invalid throttle rates.

        Asserts:
        -------
            Errors are returned for invalid throttle rates.
        """
        # Valid boolean and list settings
        # Admin settings
        mock_config.admin_has_add_permission = True
        mock_config.admin_has_change_permission = False
        mock_config.admin_has_delete_permission = True
        mock_config.admin_has_module_permission = False

        # APIKey
        mock_config.header_name = "Authorization"
        mock_config.header_type = None
        mock_config.use_caching = False
        mock_config.cache_timeout = 200
        mock_config.reset_requests_interval = None
        mock_config.max_requests = None

        # Global API settings
        mock_config.api_allow_list = True
        mock_config.api_allow_retrieve = False
        mock_config.api_allow_create = True
        mock_config.api_allow_update = True
        mock_config.api_allow_delete = True

        mock_config.view_ordering_fields = ["created_at"]
        mock_config.api_ordering_fields = [
            "max_requests",
            "requests_count",
            "created_at",
            "expires_at",
            "max_requests",
            "reset_at",
        ]
        mock_config.api_search_fields = ["id"]

        # Invalid throttle rates
        mock_config.base_user_throttle_rate = "invalid_rate"
        mock_config.staff_user_throttle_rate = "abc/hour"

        mock_config.get_setting.side_effect = lambda name, default: default

        errors = check_apikey_settings(None)
        assert (
            len(errors) == 2
        ), f"Expected 2 errors for invalid throttle rates, but got {len(errors)}"
        error_ids = [error.id for error in errors]
        expected_ids = [
            f"apikey_auth.E005_{mock_config.prefix}BASE_USER_THROTTLE_RATE",
            f"apikey_auth.E007_{mock_config.prefix}STAFF_USER_THROTTLE_RATE",
        ]
        assert all(
            eid in error_ids for eid in expected_ids
        ), f"Expected error IDs {expected_ids}, got {error_ids}"

    @patch("apikey_auth.settings.checks.config")
    def test_invalid_path_import(self, mock_config: MagicMock) -> None:
        """
        Test that invalid path import settings return errors.

        Args:
        ----
            mock_config (MagicMock): Mocked configuration object with invalid paths.

        Asserts:
        -------
            Errors are returned for invalid path imports.
        """
        # Valid boolean, list, and throttle settings
        # Admin settings
        mock_config.admin_has_add_permission = True
        mock_config.admin_has_change_permission = False
        mock_config.admin_has_delete_permission = True
        mock_config.admin_has_module_permission = False

        # APIKey
        mock_config.header_name = "Authorization"
        mock_config.header_type = None
        mock_config.use_caching = False
        mock_config.cache_timeout = 200
        mock_config.reset_requests_interval = None
        mock_config.max_requests = None

        # Global API settings
        mock_config.api_allow_list = True
        mock_config.api_allow_retrieve = False
        mock_config.api_allow_create = True
        mock_config.api_allow_update = True
        mock_config.api_allow_delete = True
        mock_config.base_user_throttle_rate = "100/day"
        mock_config.staff_user_throttle_rate = "200/hour"

        mock_config.view_ordering_fields = ["created_at"]
        mock_config.api_ordering_fields = [
            "max_requests",
            "requests_count",
            "created_at",
            "expires_at",
            "max_requests",
            "reset_at",
        ]
        mock_config.api_search_fields = ["id"]

        mock_config.get_setting.side_effect = (
            lambda name, default: "invalid.path.ClassName"
        )

        errors = check_apikey_settings(None)
        assert (
            len(errors) == 8
        ), f"Expected 8 errors for invalid paths, but got {len(errors)}"
        error_ids = [error.id for error in errors]
        expected_ids = [
            f"apikey_auth.E010_{mock_config.prefix}ADMIN_SITE_CLASS",
            f"apikey_auth.E010_{mock_config.prefix}API_APIKEY_SERIALIZER_CLASS",
            f"apikey_auth.E010_{mock_config.prefix}API_THROTTLE_CLASS",
            f"apikey_auth.E010_{mock_config.prefix}API_PAGINATION_CLASS",
            f"apikey_auth.E010_{mock_config.prefix}VIEW_PERMISSION_CLASS",
            f"apikey_auth.E010_{mock_config.prefix}API_EXTRA_PERMISSION_CLASS",
            f"apikey_auth.E011_{mock_config.prefix}API_PARSER_CLASSES",
            f"apikey_auth.E010_{mock_config.prefix}API_FILTERSET_CLASS",
        ]
        assert all(
            eid in error_ids for eid in expected_ids
        ), f"Expected error IDs {expected_ids}, got {error_ids}"
