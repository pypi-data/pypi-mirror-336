import sys

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from apikey_auth.models import APIKey
from apikey_auth.settings.conf import config
from apikey_auth.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.api,
    pytest.mark.api_views,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestAPIKeyViewSet:
    """
    Tests for the APIKeyViewSet API endpoints.

    This test class verifies the behavior of the APIKeyViewSet,
    ensuring that the list, retrieve, create, update, and destroy methods function correctly
    under various configurations and user permissions.

    Tests:
    -------
    - test_list_apikey: Verifies that the list endpoint returns a 200 OK status and includes results when allowed.
    - test_retrieve_apikey: Checks that the retrieve endpoint returns a 200 OK status and the correct API key when allowed.
    - test_create_apikey: Tests that the create endpoint returns a 201 Created status when allowed.
    - test_update_apikey: Tests that the update endpoint returns a 200 OK status when allowed.
    - test_destroy_apikey: Tests that the destroy endpoint returns a 204 No Content status when allowed.
    - test_list_apikey_disabled: Tests that the list endpoint returns a 405 Method Not Allowed status when disabled.
    - test_retrieve_apikey_disabled: Tests that the retrieve endpoint returns a 405 Method Not Allowed status when disabled.
    """

    def test_list_apikey(
        self,
        api_client: APIClient,
        apikey: APIKey,
    ):
        """
        Test the list endpoint for APIKey.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            apikey (APIKey): A sample APIKey instance to ensure data is present.

        Asserts:
        --------
            The response status code is 200.
            The response data contains a 'results' key with data.
        """
        api_client.force_authenticate(user=apikey.user)

        config.api_allow_list = True  # Ensure the list method is allowed
        config.api_extra_permission_class = None

        url = reverse("my-api-key-list")
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert "results" in response.data, "Expected 'results' in response data."
        assert len(response.data["results"]) > 0, "Expected data in the results."
        assert (
            response.data["results"][0]["key"] == apikey.key
        ), f"Expected API key {apikey.key}, got {response.data['results'][0]['key']}"

    def test_retrieve_apikey(
        self,
        api_client: APIClient,
        apikey: APIKey,
    ):
        """
        Test the retrieve endpoint for APIKey.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            apikey (APIKey): The APIKey instance to retrieve.

        Asserts:
        --------
            The response status code is 200.
            The response data contains the correct APIKey ID and key.
        """
        api_client.force_authenticate(user=apikey.user)

        config.api_allow_retrieve = True  # Ensure the retrieve method is allowed

        url = reverse("my-api-key-detail", kwargs={"pk": apikey.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."

        assert (
            response.data["id"] == apikey.pk
        ), f"Expected APIKey ID {apikey.pk}, got {response.data['id']}."
        assert (
            response.data["key"] == apikey.key
        ), f"Expected key {apikey.key}, got {response.data['key']}."

    @pytest.mark.parametrize("is_staff", [True, False])
    def test_list_apikey_disabled(
        self, api_client: APIClient, admin_user: User, user: User, is_staff: bool
    ):
        """
        Test the list view when disabled via configuration.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            user (User): A regular user for testing permissions.
            is_staff (bool): Indicates whether to authenticate as an admin or regular user.

        Asserts:
        --------
            The response status code is 405.
        """
        _user = admin_user if is_staff else user
        api_client.force_authenticate(user=_user)

        config.api_allow_list = False  # Disable the list method

        url = reverse("my-api-key-list")
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_retrieve_apikey_disabled(
        self,
        api_client: APIClient,
        admin_user: User,
        apikey: APIKey,
    ):
        """
        Test the retrieve view when disabled via configuration.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            apikey (APIKey): The APIKey instance to retrieve.

        Asserts:
        --------
            The response status code is 405.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_retrieve = False  # Disable the retrieve method

        url = reverse("my-api-key-detail", kwargs={"pk": apikey.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."
