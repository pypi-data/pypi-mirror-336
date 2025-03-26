import sys
from unittest.mock import patch

import pytest

from apikey_auth.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON
from apikey_auth.validators.config_validators import (
    validate_boolean_setting,
    validate_list_fields,
    validate_optional_path_setting,
    validate_optional_paths_setting,
    validate_throttle_rate,
    validate_string,
    validate_request_interval,
    validate_positive_integer,
)

pytestmark = [
    pytest.mark.validators,
    pytest.mark.config_validators,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestValidateBooleanSetting:
    def test_valid_boolean(self) -> None:
        """
        Test that a valid boolean setting returns no errors.

        Args:
        ----
            None

        Asserts:
        -------
            The result should have no errors.
        """
        errors = validate_boolean_setting(True, "SOME_BOOLEAN_SETTING")
        assert not errors  # No errors should be returned

    def test_invalid_boolean(self) -> None:
        """
        Test that a non-boolean setting returns an error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID.
        """
        errors = validate_boolean_setting("not_boolean", "SOME_BOOLEAN_SETTING")  # type: ignore
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E001_SOME_BOOLEAN_SETTING"


class TestValidateListFields:
    def test_valid_list(self) -> None:
        """
        Test that a valid list of fields returns no errors.

        Args:
        ----
            None

        Asserts:
        -------
            The result should have no errors.
        """
        errors = validate_list_fields(["field1", "field2"], "SOME_LIST_SETTING")
        assert not errors  # No errors should be returned

    def test_invalid_list_type(self) -> None:
        """
        Test that a non-list setting returns an error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID.
        """
        errors = validate_list_fields("not_a_list", "SOME_LIST_SETTING")  # type: ignore
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E002_SOME_LIST_SETTING"

    def test_empty_list(self) -> None:
        """
        Test that an empty list returns an error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID.
        """
        errors = validate_list_fields([], "SOME_LIST_SETTING")
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E003_SOME_LIST_SETTING"

    def test_invalid_element_in_list(self) -> None:
        """
        Test that a list containing a non-string element returns an error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID.
        """
        errors = validate_list_fields([123, "valid_field"], "SOME_LIST_SETTING")
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E004_SOME_LIST_SETTING"


class TestValidateThrottleRate:
    def test_valid_throttle_rate(self) -> None:
        """
        Test that a valid throttle rate returns no errors.

        Args:
        ----
            None

        Asserts:
        -------
            The result should have no errors.
        """
        errors = validate_throttle_rate("10/minute", "THROTTLE_RATE_SETTING")
        assert not errors

    def test_invalid_format(self) -> None:
        """
        Test that an invalid format for throttle rate returns an error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID for invalid formats.
        """
        errors = validate_throttle_rate("invalid_rate", "THROTTLE_RATE_SETTING")
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E005_THROTTLE_RATE_SETTING"

        errors = validate_throttle_rate("invalid/type/given", "THROTTLE_RATE_SETTING")
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E006_THROTTLE_RATE_SETTING"

    def test_invalid_time_unit(self) -> None:
        """
        Test that an invalid time unit in throttle rate returns an error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID for invalid time units.
        """
        errors = validate_throttle_rate("10/century", "THROTTLE_RATE_SETTING")
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E008_THROTTLE_RATE_SETTING"

    def test_non_numeric_rate(self) -> None:
        """
        Test that a non-numeric rate part returns an error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID for non-numeric rates.
        """
        errors = validate_throttle_rate("abc/minute", "THROTTLE_RATE_SETTING")
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E007_THROTTLE_RATE_SETTING"


class TestValidateOptionalClassSetting:
    def test_valid_class_import(self) -> None:
        """
        Test that a valid class path returns no errors.

        Args:
        ----
            None

        Asserts:
        -------
            The result should have no errors.
        """
        with patch("django.utils.module_loading.import_string"):
            errors = validate_optional_path_setting(
                "apikey_auth.api.throttlings.role_base_throttle.RoleBasedUserRateThrottle",
                "SOME_CLASS_SETTING",
            )
            assert not errors

    def test_invalid_class_import(self) -> None:
        """
        Test that an invalid class path returns an import error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID for invalid class paths.
        """
        with patch(
            "django.utils.module_loading.import_string", side_effect=ImportError
        ):
            errors = validate_optional_path_setting(
                "invalid.path.ClassName", "SOME_CLASS_SETTING"
            )
            assert len(errors) == 1
            assert errors[0].id == "apikey_auth.E010_SOME_CLASS_SETTING"

    def test_invalid_class_path_type(self) -> None:
        """
        Test that a non-string class path returns an error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID for non-string class paths.
        """
        errors = validate_optional_path_setting(12345, "SOME_CLASS_SETTING")  # type: ignore
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E009_SOME_CLASS_SETTING"

    def test_none_class_path(self) -> None:
        """
        Test that a None class path returns no error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should have no errors.
        """
        errors = validate_optional_path_setting(None, "SOME_CLASS_SETTING")  # type: ignore
        assert not errors

    def test_invalid_list_args_classes_import(self) -> None:
        """
        Test that a list of invalid classes args returns an error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain errors for each invalid class path with the expected error ID.
        """
        errors = validate_optional_paths_setting([1, 5], "SOME_CLASS_SETTING")
        assert len(errors) == 2
        assert errors[0].id == "apikey_auth.E012_SOME_CLASS_SETTING"

    def test_invalid_path_classes_import(self) -> None:
        """
        Test that a list of invalid classes path returns an import error.

        Args:
        ----
            None

        Asserts:
        -------
            The result should contain one error with the expected error ID for invalid class paths.
        """
        with patch(
            "django.utils.module_loading.import_string", side_effect=ImportError
        ):
            errors = validate_optional_paths_setting(
                ["INVALID_PATH"], "SOME_CLASS_SETTING"
            )
            assert len(errors) == 1
            assert errors[0].id == "apikey_auth.E013_SOME_CLASS_SETTING"


class TestValidatePositiveInteger:
    def test_valid_positive_integer(self) -> None:
        """Test that a valid positive integer returns no errors."""
        errors = validate_positive_integer(5, "POSITIVE_INTEGER_SETTING")
        assert not errors  # No errors should be returned

    def test_invalid_negative_integer(self) -> None:
        """Test that a negative integer returns an error."""
        errors = validate_positive_integer(-1, "POSITIVE_INTEGER_SETTING")
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E014_POSITIVE_INTEGER_SETTING"

    def test_invalid_zero(self) -> None:
        """Test that zero returns an error."""
        errors = validate_positive_integer(0, "POSITIVE_INTEGER_SETTING")
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E014_POSITIVE_INTEGER_SETTING"

    def test_invalid_non_integer(self) -> None:
        """Test that a non-integer value returns an error."""
        errors = validate_positive_integer("not_an_integer", "POSITIVE_INTEGER_SETTING")  # type: ignore
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E014_POSITIVE_INTEGER_SETTING"

    def test_none_value_with_allow_none(self) -> None:
        """Test that None value with allow_none=True returns no errors."""
        errors = validate_positive_integer(
            None, "POSITIVE_INTEGER_SETTING", allow_none=True
        )
        assert not errors  # No errors should be returned

    def test_none_value_without_allow_none(self) -> None:
        """Test that None value without allow_none returns an error."""
        errors = validate_positive_integer(
            None, "POSITIVE_INTEGER_SETTING", allow_none=False
        )
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E014_POSITIVE_INTEGER_SETTING"


class TestValidateRequestInterval:
    def test_valid_request_interval(self) -> None:
        """Test that a valid request interval returns no errors."""
        errors = validate_request_interval("daily", "REQUEST_INTERVAL_SETTING")
        assert not errors  # No errors should be returned

    def test_invalid_request_interval(self) -> None:
        """Test that an invalid request interval returns an error."""
        errors = validate_request_interval("weekly", "REQUEST_INTERVAL_SETTING")
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E016_REQUEST_INTERVAL_SETTING"

    def test_invalid_type(self) -> None:
        """Test that a non-string request interval returns an error."""
        errors = validate_request_interval(123, "REQUEST_INTERVAL_SETTING")  # type: ignore
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E015_REQUEST_INTERVAL_SETTING"

    def test_none_value(self) -> None:
        """Test that None value returns no errors."""
        errors = validate_request_interval(None, "REQUEST_INTERVAL_SETTING")
        assert not errors  # No errors should be returned


class TestValidateString:
    def test_valid_string(self) -> None:
        """Test that a valid string returns no errors."""
        errors = validate_string("valid_string", "STRING_SETTING")
        assert not errors  # No errors should be returned

    def test_invalid_type(self) -> None:
        """Test that a non-string value returns an error."""
        errors = validate_string(123, "STRING_SETTING")  # type: ignore
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E017_STRING_SETTING"

    def test_none_value_without_allow_none(self) -> None:
        """Test that None value without allow_none returns an error."""
        errors = validate_string(None, "STRING_SETTING", allow_none=False)
        assert len(errors) == 1
        assert errors[0].id == "apikey_auth.E017_STRING_SETTING"

    def test_none_value_with_allow_none(self) -> None:
        """Test that None value with allow_none=True returns no errors."""
        errors = validate_string(None, "STRING_SETTING", allow_none=True)
        assert not errors  # No errors should be returned
