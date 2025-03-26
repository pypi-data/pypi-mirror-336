from typing import Any, List

from django.core.checks import Error, register

from apikey_auth.settings.conf import config
from apikey_auth.validators.config_validators import (
    validate_boolean_setting,
    validate_list_fields,
    validate_optional_path_setting,
    validate_optional_paths_setting,
    validate_positive_integer,
    validate_request_interval,
    validate_string,
    validate_throttle_rate,
)


@register()
def check_apikey_settings(app_configs: Any, **kwargs: Any) -> List[Error]:
    """Check and validate system monitor settings in the Django configuration.

    This function performs validation of various system monitor-related settings
    defined in the Django settings. It returns a list of errors if any issues are found.

    Parameters:
    -----------
    app_configs : Any
        Passed by Django during checks (not used here).

    kwargs : Any
        Additional keyword arguments for flexibility.

    Returns:
    --------
    List[Error]
        A list of `Error` objects for any detected configuration issues.

    """
    errors: List[Error] = []

    # Validate Admin settings
    errors.extend(
        validate_boolean_setting(
            config.admin_has_add_permission, f"{config.prefix}ADMIN_HAS_ADD_PERMISSION"
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.admin_has_change_permission,
            f"{config.prefix}ADMIN_HAS_CHANGE_PERMISSION",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.admin_has_delete_permission,
            f"{config.prefix}ADMIN_HAS_DELETE_PERMISSION",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.admin_has_module_permission,
            f"{config.prefix}ADMIN_HAS_MODULE_PERMISSION",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}ADMIN_SITE_CLASS", None),
            f"{config.prefix}ADMIN_SITE_CLASS",
        )
    )

    # Validate APIKey settings
    errors.extend(
        validate_request_interval(
            config.reset_requests_interval, f"{config.prefix}RESET_REQUEST_INTERVAL"
        )
    )
    errors.extend(
        validate_positive_integer(
            config.max_requests, f"{config.prefix}MAX_REQUESTS", allow_none=True
        )
    )
    errors.extend(
        validate_boolean_setting(config.use_caching, f"{config.prefix}USE_CACHING")
    )
    errors.extend(
        validate_positive_integer(
            config.cache_timeout, f"{config.prefix}CACHE_TIMEOUT_SECONDS"
        )
    )
    errors.extend(validate_string(config.header_name, f"{config.prefix}HEADER_NAME"))
    errors.extend(
        validate_string(
            config.header_type, f"{config.prefix}HEADER_TYPE", allow_none=True
        )
    )

    # Validate Global API settings
    errors.extend(
        validate_boolean_setting(
            config.api_allow_list, f"{config.prefix}API_ALLOW_LIST"
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_allow_retrieve, f"{config.prefix}API_ALLOW_RETRIEVE"
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_allow_create, f"{config.prefix}API_ALLOW_CREATE"
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_allow_update, f"{config.prefix}API_ALLOW_UPDATE"
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_allow_delete, f"{config.prefix}API_ALLOW_DELETE"
        )
    )
    errors.extend(
        validate_throttle_rate(
            config.base_user_throttle_rate, f"{config.prefix}BASE_USER_THROTTLE_RATE"
        )
    )
    errors.extend(
        validate_throttle_rate(
            config.staff_user_throttle_rate, f"{config.prefix}STAFF_USER_THROTTLE_RATE"
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_ordering_fields, f"{config.prefix}API_ORDERING_FIELDS"
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_search_fields, f"{config.prefix}API_SEARCH_FIELDS"
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_THROTTLE_CLASS", None),
            f"{config.prefix}API_THROTTLE_CLASS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_APIKEY_SERIALIZER_CLASS", None),
            f"{config.prefix}API_APIKEY_SERIALIZER_CLASS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_PAGINATION_CLASS", None),
            f"{config.prefix}API_PAGINATION_CLASS",
        )
    )
    errors.extend(
        validate_optional_paths_setting(
            config.get_setting(f"{config.prefix}API_PARSER_CLASSES", None),
            f"{config.prefix}API_PARSER_CLASSES",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_FILTERSET_CLASS", None),
            f"{config.prefix}API_FILTERSET_CLASS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_EXTRA_PERMISSION_CLASS", None),
            f"{config.prefix}API_EXTRA_PERMISSION_CLASS",
        )
    )

    # Validate Template View settings
    errors.extend(
        validate_list_fields(
            config.view_ordering_fields, f"{config.prefix}VIEW_ORDERING_FIELDS"
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}VIEW_PERMISSION_CLASS", None),
            f"{config.prefix}VIEW_PERMISSION_CLASS",
        )
    )

    return errors
