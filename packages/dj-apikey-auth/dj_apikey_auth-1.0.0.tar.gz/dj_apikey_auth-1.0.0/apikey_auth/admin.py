from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .mixins.admin.permission import AdminPermissionControlMixin
from .models import APIKey
from .settings.conf import config


@admin.register(APIKey, site=config.admin_site_class)
class APIKeyAdmin(AdminPermissionControlMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "user_display",
        "is_active",
        "requests_count",
        "max_requests",
        "status",
    )
    list_display_links = ("id", "user_display")
    autocomplete_fields = ("user",)
    search_fields = ("key",)
    list_filter = ("is_active", "expires_at", "reset_at")
    list_editable = ("is_active",)
    readonly_fields = ("key", "created_at", "reset_at")
    date_hierarchy = "expires_at"
    actions = ["activate_keys", "deactivate_keys"]
    fieldsets = (
        (None, {"fields": ("user", "key", "created_at")}),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                    "expires_at",
                    "requests_count",
                    "max_requests",
                    "reset_at",
                ),
            },
        ),
    )

    def user_display(self, obj):
        """Show the user associated with the API key or 'Anonymous' if null."""
        return obj.user if obj.user else _("Anonymous")

    user_display.short_description = _("User")

    def status(self, obj):
        """Show the API key status with colors."""
        criteria = obj.is_active and not obj.has_expired()
        color = "green" if criteria else "red"
        status_text = _("Active") if criteria else _("Inactive")
        return format_html('<b style="color: {};">{}</b>', color, status_text)

    status.short_description = _("Status")

    def activate_keys(self, request, queryset):
        """Activate selected API keys."""
        updated = queryset.update(is_active=True)
        self.message_user(request, _(f"{updated} {_('API keys activated.')}"))

    activate_keys.short_description = _("Activate selected API keys")

    def deactivate_keys(self, request, queryset):
        """Deactivate selected API keys."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} {_('API keys deactivated.')}")

    deactivate_keys.short_description = _("Deactivate selected API keys")
