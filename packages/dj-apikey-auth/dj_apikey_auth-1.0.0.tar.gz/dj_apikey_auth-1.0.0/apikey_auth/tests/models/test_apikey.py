import sys
from datetime import timedelta

import pytest
from django.utils.timezone import now

from apikey_auth.models import APIKey
from apikey_auth.settings.conf import config
from apikey_auth.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestAPIKeyModel:
    """
    Test suite for the APIKey model.
    """

    def test_str_method(self, apikey: APIKey) -> None:
        """
        Test that the __str__ method returns the correct string representation of an API key.

        Asserts:
        -------
            - The string representation includes the URL and timestamp.
        """
        user_id = apikey.user_id or "Anonymous"
        expected_str = f"User ID: {user_id} - {apikey.key[:10]}..."
        assert (
            str(apikey) == expected_str
        ), f"Expected the __str__ method to return '{expected_str}', but got '{str(apikey)}'."

    def test_has_expired_with_future_expiration(self, apikey: APIKey) -> None:
        """
        Test that has_expired returns False when the expiration date is in the future.

        Asserts:
            - has_expired returns False for an API key with a future expiration date.
        """
        apikey.expires_at = now() + timedelta(days=1)
        assert (
            not apikey.has_expired()
        ), "Expected has_expired to return False for a future expiration date."

    def test_has_expired_with_past_expiration(self, apikey: APIKey) -> None:
        """
        Test that has_expired returns True when the expiration date is in the past.

        Asserts:
            - has_expired returns True for an API key with a past expiration date.
        """
        apikey.expires_at = now() - timedelta(days=1)
        assert (
            apikey.has_expired()
        ), "Expected has_expired to return True for a past expiration date."

    def test_has_expired_with_no_expiration(self, apikey: APIKey) -> None:
        """
        Test that has_expired returns False when there is no expiration date.

        Asserts:
            - has_expired returns False for an API key with no expiration date.
        """
        apikey.expires_at = None
        assert (
            not apikey.has_expired()
        ), "Expected has_expired to return False for no expiration date."

    def test_reset_requests_with_past_reset_at(self, apikey: APIKey) -> None:
        """
        Test that reset_requests resets the request count and updates reset_at when reset_at is in the past.

        Asserts:
            - requests_count is reset to 0.
            - reset_at is updated to a future datetime.
        """
        config.reset_requests_interval = "minutely"
        apikey.reset_at = now() - timedelta(minutes=1)
        apikey.requests_count = 10
        apikey.reset_requests()
        assert apikey.requests_count == 0, "Expected requests_count to be reset to 0."
        assert (
            apikey.reset_at > now()
        ), "Expected reset_at to be updated to a future datetime."

    def test_reset_requests_with_future_reset_at(self, apikey: APIKey) -> None:
        """
        Test that reset_requests does nothing when reset_at is in the future.

        Asserts:
            - requests_count remains unchanged.
            - reset_at remains unchanged.
        """
        original_reset_at = apikey.reset_at
        apikey.requests_count = 10
        apikey.reset_requests()
        assert (
            apikey.requests_count == 10
        ), "Expected requests_count to remain unchanged."
        assert (
            apikey.reset_at == original_reset_at
        ), "Expected reset_at to remain unchanged."

    def test_increment_requests_within_limit(self, apikey: APIKey) -> None:
        """
        Test that increment_requests increments the request count and returns True when within the limit.

        Asserts:
            - requests_count is incremented by 1.
            - The method returns True.
        """
        apikey.max_requests = 10
        apikey.requests_count = 5
        result = apikey.increment_requests()
        assert (
            apikey.requests_count == 6
        ), "Expected requests_count to be incremented to 6."
        assert (
            result
        ), "Expected increment_requests to return True when within the limit."

    def test_increment_requests_exceeds_limit(self, apikey: APIKey) -> None:
        """
        Test that increment_requests increments the request count and returns False when exceeding the limit.

        Asserts:
            - requests_count is incremented by 1.
            - The method returns False.
        """
        apikey.max_requests = 10
        apikey.requests_count = 10
        result = apikey.increment_requests()
        assert (
            apikey.requests_count == 11
        ), "Expected requests_count to be incremented to 11."
        assert (
            not result
        ), "Expected increment_requests to return False when exceeding the limit."

    def test_calculate_next_reset_minutely(self, monkeypatch) -> None:
        """
        Test that calculate_next_reset returns the correct datetime for a minutely interval.

        Asserts:
            - The returned datetime is 1 minute in the future.
        """
        monkeypatch.setattr(config, "reset_requests_interval", "minutely")
        next_reset = APIKey.calculate_next_reset()
        assert next_reset <= now() + timedelta(
            minutes=1
        ), "Expected next_reset to be 1 minute in the future."

    def test_calculate_next_reset_hourly(self, monkeypatch) -> None:
        """
        Test that calculate_next_reset returns the correct datetime for an hourly interval.

        Asserts:
            - The returned datetime is 1 hour in the future.
        """
        monkeypatch.setattr(config, "reset_requests_interval", "hourly")
        next_reset = APIKey.calculate_next_reset()
        assert next_reset <= now() + timedelta(
            hours=1
        ), "Expected next_reset to be 1 hour in the future."

    def test_calculate_next_reset_daily(self, monkeypatch) -> None:
        """
        Test that calculate_next_reset returns the correct datetime for a daily interval.

        Asserts:
            - The returned datetime is 1 day in the future.
        """
        monkeypatch.setattr(config, "reset_requests_interval", "daily")
        next_reset = APIKey.calculate_next_reset()
        assert next_reset <= now() + timedelta(
            days=1
        ), "Expected next_reset to be 1 day in the future."

    def test_calculate_next_reset_monthly(self, monkeypatch) -> None:
        """
        Test that calculate_next_reset returns the correct datetime for a monthly interval.

        Asserts:
            - The returned datetime is approximately 30 days in the future.
        """
        monkeypatch.setattr(config, "reset_requests_interval", "monthly")
        next_reset = APIKey.calculate_next_reset()
        assert next_reset <= now() + timedelta(
            days=30
        ), "Expected next_reset to be approximately 30 days in the future."

    def test_calculate_next_reset_no_interval(self, monkeypatch) -> None:
        """
        Test that calculate_next_reset returns None when no interval is configured.

        Asserts:
            - The returned value is None.
        """
        monkeypatch.setattr(config, "reset_requests_interval", None)
        next_reset = APIKey.calculate_next_reset()
        assert (
            next_reset is None
        ), "Expected next_reset to be None when no interval is configured."

    def test_calculate_next_reset_invalid_interval(self, monkeypatch) -> None:
        """
        Test that calculate_next_reset returns default value when invalid interval is configured.

        Asserts:
            - The returned value is default value.
        """
        monkeypatch.setattr(config, "reset_requests_interval", "invalid")
        next_reset = APIKey.calculate_next_reset()
        assert next_reset <= now() + timedelta(
            days=1
        ), "Expected next_reset to be approximately 1 day in the future."
