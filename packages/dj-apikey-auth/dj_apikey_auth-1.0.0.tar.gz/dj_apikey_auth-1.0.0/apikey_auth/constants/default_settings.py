from dataclasses import dataclass, field
from typing import List, Optional

from apikey_auth.utils.user_model import REQUIRED_FIELDS, USERNAME_FIELD


@dataclass(frozen=True)
class DefaultAdminSettings:
    admin_site_class: Optional[str] = None
    admin_has_add_permission: bool = True
    admin_has_change_permission: bool = True
    admin_has_delete_permission: bool = True
    admin_has_module_permission: bool = True


@dataclass(frozen=True)
class DefaultThrottleSettings:
    base_user_throttle_rate: str = "30/minute"
    staff_user_throttle_rate: str = "100/minute"
    throttle_class: str = "apikey_auth.api.throttlings.RoleBasedUserRateThrottle"


@dataclass(frozen=True)
class DefaultPaginationAndFilteringSettings:
    pagination_class: str = "apikey_auth.api.paginations.DefaultLimitOffSetPagination"
    filterset_class: Optional[str] = None
    ordering_fields: List[str] = field(
        default_factory=lambda: [
            "max_requests",
            "requests_count",
            "created_at",
            "expires_at",
            "max_requests",
            "reset_at",
        ]
    )
    search_fields: List[str] = field(default_factory=lambda: ["id"])


@dataclass(frozen=True)
class DefaultSerializerSettings:
    user_serializer_class: Optional[str] = None
    apikey_serializer_class: Optional[str] = None
    user_serializer_fields: List[str] = field(
        default_factory=lambda: [USERNAME_FIELD] + list(REQUIRED_FIELDS)
    )


@dataclass(frozen=True)
class DefaultAPISettings:
    allow_list: bool = True
    allow_retrieve: bool = True
    allow_create: bool = True
    allow_update: bool = True
    allow_delete: bool = False
    extra_permission_class: Optional[str] = None
    parser_classes: List[str] = field(
        default_factory=lambda: [
            "rest_framework.parsers.JSONParser",
            "rest_framework.parsers.MultiPartParser",
            "rest_framework.parsers.FormParser",
        ]
    )


@dataclass(frozen=True)
class DefaultAPIKeySettings:
    request_reset_interval: Optional[str] = None
    max_requests: Optional[int] = None
    header_name: str = "Authorization"
    header_type: Optional[str] = None
    use_caching: bool = False
    cache_timeout: int = 300


@dataclass(frozen=True)
class DefaultViewSettings:
    permission_class: Optional[str] = "rest_framework.permissions.IsAdminUser"
    ordering_fields: List[str] = field(
        default_factory=lambda: ["expires_at", "-created_at"]
    )


admin_settings = DefaultAdminSettings()
throttle_settings = DefaultThrottleSettings()
pagination_and_filter_settings = DefaultPaginationAndFilteringSettings()
serializer_settings = DefaultSerializerSettings()
api_settings = DefaultAPISettings()
apikey_settings = DefaultAPIKeySettings()
view_settings = DefaultViewSettings()
