from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apikey_auth.api.serializers.helper.get_serializer_cls import user_serializer_class
from apikey_auth.models import APIKey
from apikey_auth.utils.user_model import UserModel


class APIKeySerializer(serializers.ModelSerializer):
    user = user_serializer_class()(read_only=True)
    user_id = serializers.IntegerField(
        allow_null=True,
        required=False,
        write_only=True,
        label=_("User ID"),
        help_text=_("The ID of the user associated with this APIKey (Optional)"),
    )

    class Meta:
        model = APIKey
        fields = [
            "id",
            "user_id",
            "user",
            "key",
            "created_at",
            "expires_at",
            "is_active",
            "requests_count",
            "max_requests",
            "reset_at",
        ]
        read_only_fields = [
            "id",
            "key",
            "created_at",
            "requests_count",
            "max_requests",
            "reset_at",
        ]

    def create(self, validated_data):
        """Ensure API key is generated on creation with the validated user."""
        user_id = validated_data.pop(
            "user_id", None
        )  # Remove user_id from validated_data
        if user_id:
            try:
                user = UserModel.objects.get(id=user_id)
            except UserModel.DoesNotExist:
                raise serializers.ValidationError(
                    {"user_id": _("User with the provided user_id does not exist.")}
                )
            validated_data["user"] = user
        return super().create(validated_data)
