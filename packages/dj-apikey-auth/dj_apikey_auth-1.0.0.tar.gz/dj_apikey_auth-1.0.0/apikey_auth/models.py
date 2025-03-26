import secrets
from datetime import datetime, timedelta
from typing import Optional

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from apikey_auth.settings.conf import config


class APIKey(models.Model):
    """A model to manage API keys for authentication and rate limiting.

    This model stores API keys associated with users, tracks request counts, and enforces
    rate limits based on configurable intervals (minutely, hourly, daily, monthly).
    It also supports optional expiration dates and active/inactive status for keys.

    Fields:
        user (ForeignKey): The user who owns this API key. Can be null for anonymous keys.
        key (CharField): A unique, secure API key used for authentication.
        created_at (DateTimeField): The timestamp when the API key was created.
        expires_at (DateTimeField): Optional expiration date for the API key.
        is_active (BooleanField): Indicates whether the API key is active and usable.
        requests_count (PositiveIntegerField): Tracks the number of requests made with this key.
        max_requests (PositiveIntegerField): Maximum allowed requests (total or per reset period).
        reset_at (DateTimeField): Timestamp when the request count will reset (if applicable).

    Methods:
        __str__(): Returns a human-readable representation of the API key.
        save(): Generates a secure API key and sets defaults if not provided.
        has_expired(): Checks if the API key has expired based on its expiration date.
        reset_requests(): Resets the request count if the reset time has passed.
        increment_requests(): Increments the request count and checks if the limit is exceeded.
        calculate_next_reset(): Calculates the next reset time based on the configured interval.

    Meta:
        verbose_name: Human-readable name for the model (singular).
        verbose_name_plural: Human-readable name for the model (plural).
        ordering: Default ordering for queries (newest first).
        db_table_comment: Description of the table for database documentation.

    """

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="api_keys",
        null=True,
        blank=True,
        verbose_name=_("User"),
        help_text=_("The user who owns this API key."),
        db_comment="The user associated with this API key.",
    )
    key = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
        verbose_name=_("API Key"),
        help_text=_("A unique API key used for authentication."),
        db_comment="The API key used for authentication.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
        help_text=_("The date and time when the API key was created."),
        db_comment="Timestamp when the API key was generated.",
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Expiration Date"),
        help_text=_(
            "The date and time when the API key will expire. Leave blank for no expiration."
        ),
        db_comment="Optional expiration date for the API key.",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Indicates whether the API key is currently active and usable."),
        db_comment="Status flag to enable or disable the API key.",
    )
    requests_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Requests Count"),
        help_text=_("Number of requests made with this API key."),
        db_comment="Tracks the total number of requests made using this API key.",
    )
    max_requests = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Max Requests"),
        help_text=_("Maximum number of requests allowed (total or per reset period)."),
        db_comment="Defines the maximum allowed requests, either total or per reset interval.",
    )
    reset_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Reset at"),
        help_text=_("Time when the request count resets (if applicable)."),
        db_comment="Timestamp when the request count will reset, if rate limiting is time-based.",
    )

    class Meta:
        verbose_name = _("API Key")
        verbose_name_plural = _("API Keys")
        ordering = ["-created_at"]
        db_table_comment = (
            "Table storing API keys for authentication and rate limiting."
        )

    def __str__(self) -> str:
        """Return a string representation of the API key.

        Includes the associated user ID (or 'Anonymous' if none) and the first 10 characters
        of the key followed by an ellipsis.

        Returns:
            str: A human-readable representation of the API key instance.

        """
        user_id = self.user_id or _("Anonymous")
        return f"{_('User ID')}: {user_id} - {self.key[:10]}..."

    def save(self, *args, **kwargs) -> None:
        """Save the API key instance, generating a secure key and setting
        defaults if needed.

        If the key is not set, generates a secure API key using secrets.token_urlsafe(),
        sets max_requests from config, and calculates the next reset time.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments passed to the parent save method.

        """
        if not self.key:
            self.key = secrets.token_urlsafe(48)
            self.max_requests = config.max_requests
            self.reset_at = self.calculate_next_reset()
        super().save(*args, **kwargs)

    def has_expired(self) -> bool:
        """Check if the API key has expired based on its expiration date.

        Returns:
            bool: True if the key has an expiration date, and it is in the past, False otherwise.

        """
        return self.expires_at is not None and self.expires_at < now()

    def reset_requests(self) -> None:
        """Reset the request count to zero if the reset time has passed.

        If reset_at is set and the current time is past reset_at, resets
        requests_count to 0 and calculates the next reset time based on
        the configured interval.

        """
        if self.reset_at and now() >= self.reset_at:
            self.requests_count = 0
            self.reset_at = self.calculate_next_reset()
            self.save(update_fields=["requests_count", "reset_at"])

    def increment_requests(self) -> bool:
        """Increment the request count and check if the limit is exceeded.

        Calls reset_requests() to check if a reset is needed first, then increments
        requests_count and saves the change. Returns whether the limit is still respected.

        Returns:
            bool: True if requests_count is within max_requests, False otherwise.

        """
        self.reset_requests()  # Check if reset is needed first
        self.requests_count += 1
        self.save(update_fields=["requests_count"])
        return self.max_requests is None or self.requests_count <= self.max_requests

    @staticmethod
    def calculate_next_reset() -> Optional[datetime]:
        """Calculate the next reset time based on the configured reset
        interval.

        Uses the reset_requests_interval from config to determine the interval
        (minutely, hourly, daily, monthly, or None). Returns None if no interval is set.

        Returns:
            Optional[datetime]: The next reset time or None if no reset interval is configured.

        """
        interval = config.reset_requests_interval
        if not interval:
            return None

        if interval == "minutely":
            return now() + timedelta(minutes=1)
        if interval == "hourly":
            return now() + timedelta(hours=1)
        elif interval == "daily":
            return now() + timedelta(days=1)
        elif interval == "monthly":
            return now() + timedelta(days=30)  # Approximation for a month
        return now() + timedelta(days=1)  # Default to daily due to invalid interval
