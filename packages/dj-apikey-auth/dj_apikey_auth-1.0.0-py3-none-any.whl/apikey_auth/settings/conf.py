from typing import Any, List, Optional

from django.conf import settings
from django.utils.module_loading import import_string

from apikey_auth.constants.default_settings import (
    admin_settings,
    api_settings,
    apikey_settings,
    pagination_and_filter_settings,
    serializer_settings,
    throttle_settings,
    view_settings,
)
from apikey_auth.constants.types import DefaultPath, OptionalPaths


class APIKeyAuthConfig:
    """A configuration handler.

    allowing dynamic settings loading from the Django settings, with
    default fallbacks.

    """

    prefix = "APIKEY_AUTH_"

    def __init__(self) -> None:
        # Admin settings
        self.admin_has_add_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_ADD_PERMISSION",
            admin_settings.admin_has_add_permission,
        )
        self.admin_has_change_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_CHANGE_PERMISSION",
            admin_settings.admin_has_change_permission,
        )
        self.admin_has_delete_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_DELETE_PERMISSION",
            admin_settings.admin_has_delete_permission,
        )
        self.admin_has_module_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_MODULE_PERMISSION",
            admin_settings.admin_has_module_permission,
        )
        # Admin site class
        self.admin_site_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}ADMIN_SITE_CLASS",
            admin_settings.admin_site_class,
        )

        # APIKey
        self.reset_requests_interval: Optional[str] = self.get_setting(
            f"{self.prefix}RESET_REQUEST_INTERVAL",
            apikey_settings.request_reset_interval,
        )
        self.max_requests: Optional[int] = self.get_setting(
            f"{self.prefix}MAX_REQUESTS", apikey_settings.max_requests
        )

        # Authentication
        self.header_name: str = self.get_setting(
            f"{self.prefix}HEADER_NAME", apikey_settings.header_name
        )
        self.header_type: str = self.get_setting(
            f"{self.prefix}HEADER_TYPE", apikey_settings.header_type
        )
        self.use_caching = self.get_setting(
            f"{self.prefix}USE_CACHING", apikey_settings.use_caching
        )
        self.cache_timeout = self.get_setting(
            f"{self.prefix}CACHE_TIMEOUT_SECONDS", apikey_settings.cache_timeout
        )

        # Global API settings
        self.api_allow_list: bool = self.get_setting(
            f"{self.prefix}API_ALLOW_LIST", api_settings.allow_list
        )
        self.api_allow_retrieve: bool = self.get_setting(
            f"{self.prefix}API_ALLOW_RETRIEVE", api_settings.allow_retrieve
        )
        self.api_allow_create: bool = self.get_setting(
            f"{self.prefix}API_ALLOW_CREATE", api_settings.allow_create
        )
        self.api_allow_update: bool = self.get_setting(
            f"{self.prefix}API_ALLOW_UPDATE", api_settings.allow_update
        )
        self.api_allow_delete: bool = self.get_setting(
            f"{self.prefix}API_ALLOW_DELETE", api_settings.allow_delete
        )
        self.base_user_throttle_rate: str = self.get_setting(
            f"{self.prefix}BASE_USER_THROTTLE_RATE",
            throttle_settings.base_user_throttle_rate,
        )
        self.staff_user_throttle_rate: str = self.get_setting(
            f"{self.prefix}STAFF_USER_THROTTLE_RATE",
            throttle_settings.staff_user_throttle_rate,
        )
        self.api_throttle_classes: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_THROTTLE_CLASS",
            throttle_settings.throttle_class,
        )
        self.api_pagination_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_PAGINATION_CLASS",
            pagination_and_filter_settings.pagination_class,
        )
        self.api_extra_permission_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_EXTRA_PERMISSION_CLASS",
            api_settings.extra_permission_class,
        )
        self.api_parser_classes: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_PARSER_CLASSES",
            api_settings.parser_classes,
        )
        self.apikey_serializer_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_APIKEY_SERIALIZER_CLASS",
            serializer_settings.apikey_serializer_class,
        )
        self.user_serializer_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_USER_SERIALIZER_CLASS",
            serializer_settings.user_serializer_class,
        )
        self.user_serializer_fields: List[str] = self.get_setting(
            f"{self.prefix}API_USER_SERIALIZER_FIELDS",
            serializer_settings.user_serializer_fields,
        )
        self.api_ordering_fields: List[str] = self.get_setting(
            f"{self.prefix}API_ORDERING_FIELDS",
            pagination_and_filter_settings.ordering_fields,
        )
        self.api_search_fields: List[str] = self.get_setting(
            f"{self.prefix}API_SEARCH_FIELDS",
            pagination_and_filter_settings.search_fields,
        )
        self.api_filterset_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_FILTERSET_CLASS",
            pagination_and_filter_settings.filterset_class,
        )

        # Template settings
        self.view_permission_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}VIEW_PERMISSION_CLASS",
            view_settings.permission_class,
        )
        self.view_ordering_fields: List[str] = self.get_setting(
            f"{self.prefix}VIEW_ORDERING_FIELDS",
            view_settings.ordering_fields,
        )

    def get_setting(self, setting_name: str, default_value: Any) -> Any:
        """Retrieve a setting from Django settings with a default fallback.

        Args:
            setting_name (str): The name of the setting to retrieve.
            default_value (Any): The default value to return if the setting is not found.

        Returns:
            Any: The value of the setting or the default value if not found.

        """
        return getattr(settings, setting_name, default_value)

    def get_optional_paths(
        self,
        setting_name: str,
        default_path: DefaultPath,
    ) -> OptionalPaths:
        """Dynamically load a method or class path on a setting, or return None
        if the setting is None or invalid.

        Args:
            setting_name (str): The name of the setting for the method or class path.
            default_path (Optional[Union[str, List[str]]): The default import path for the method or class.

        Returns:
            Optional[Union[Type[Any], List[Type[Any]]]]: The imported method or class or None
             if import fails or the path is invalid.

        """
        _path: DefaultPath = self.get_setting(setting_name, default_path)

        if _path and isinstance(_path, str):
            try:
                return import_string(_path)
            except ImportError:
                return None
        elif _path and isinstance(_path, list):
            try:
                return [import_string(path) for path in _path if isinstance(path, str)]
            except ImportError:
                return []

        return None


# Create a global config object
config: APIKeyAuthConfig = APIKeyAuthConfig()
