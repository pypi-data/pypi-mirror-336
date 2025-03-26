import sys

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from apikey_auth.api.permissions import HasAPIKey
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
        admin_user: User,
    ):
        """
        Test the list endpoint for APIKey.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            apikey (APIKey): The APIKey instance to delete.
            admin_user (User): A admin User instance to authenticate with it.

        Asserts:
        --------
            The response status code is 200.
            The response data contains a 'results' key with data.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_list = True  # Ensure the list method is allowed

        url = reverse("api-key-list")
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert "results" in response.data, "Expected 'results' in response data."
        assert len(response.data["results"]) > 0, "Expected data in the results."

    def test_retrieve_apikey(
        self, api_client: APIClient, apikey: APIKey, admin_user: User
    ):
        """
        Test the retrieve endpoint for APIKey.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            apikey (APIKey): The APIKey instance to retrieve.
            admin_user (User): A admin User instance to authenticate with it.

        Asserts:
        --------
            The response status code is 200.
            The response data contains the correct APIKey ID and key.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_retrieve = True  # Ensure the retrieve method is allowed

        url = reverse("api-key-detail", kwargs={"pk": apikey.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."

        assert (
            response.data["id"] == apikey.pk
        ), f"Expected APIKey ID {apikey.pk}, got {response.data['id']}."

    def test_create_apikey(
        self,
        api_client: APIClient,
        admin_user: User,
    ):
        """
        Test the create endpoint for APIKey.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.

        Asserts:
        --------
            The response status code is 201.
            The response data contains the created APIKey's key.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_create = True  # Ensure the create method is allowed

        url = reverse("api-key-list")
        response = api_client.post(url, {}, format="json")

        assert (
            response.status_code == 201
        ), f"Expected 201 Created, got {response.status_code}."
        assert "key" in response.data, "Expected 'key' in response data."
        assert APIKey.objects.count() == 1, "Expected one APIKey to be created"

    def test_create_apikey_invalid_user_id(
        self,
        api_client: APIClient,
        admin_user: User,
    ):
        """
        Test the create endpoint with an invalid user_id.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.

        Asserts:
        --------
            The response status code is 400 Bad Request.
            The response data contains a validation error for user_id.
            No API key is created in the database.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_create = True  # Ensure the create method is allowed

        url = reverse("api-key-list")
        invalid_user_id = 9999  # Assuming this ID doesn’t exist
        data = {"user_id": invalid_user_id}
        response = api_client.post(url, data, format="json")

        assert (
            response.status_code == 400
        ), f"Expected 400 Bad Request, got {response.status_code} with response: {response.data}"

        assert "user_id" in response.data, "Expected 'user_id' in error response."
        assert "User with the provided user_id does not exist." in str(
            response.data["user_id"]
        ), f"Expected user_id error, got {response.data['user_id']}"
        assert (
            APIKey.objects.count() == 0
        ), "No API key should be created with invalid user_id."

    def test_create_apikey_valid_user_id(
        self,
        api_client: APIClient,
        admin_user: User,
        user: User,  # Regular user fixture
    ):
        """
        Test the create endpoint with a valid user_id.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            user (User): A regular user whose ID will be used.

        Asserts:
        --------
            The response status code is 201 Created.
            The response data contains the created APIKey's key and correct user.
            The API key is created in the database with the specified user.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_create = True  # Ensure the create method is allowed

        url = reverse("api-key-list")
        data = {"user_id": user.id}  # Use a valid user ID
        response = api_client.post(url, data, format="json")

        assert (
            response.status_code == 201
        ), f"Expected 201 Created, got {response.status_code} with response: {response.data}"
        assert "key" in response.data, "Expected 'key' in response data."
        assert "user" in response.data, "Expected 'user' in response data."
        assert (
            response.data["user"] is not None
        ), f"Expected user object, got {response.data['user']}"
        assert APIKey.objects.count() == 1, "Expected one API key to be created."
        created_key = APIKey.objects.first()
        assert (
            created_key.user == user
        ), f"Expected API key user {user}, got {created_key.user}"

    def test_update_apikey(
        self, api_client: APIClient, apikey: APIKey, admin_user: User
    ):
        """
        Test the update endpoint for APIKey.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            apikey (APIKey): The APIKey instance to update.
            admin_user (User): The admin user for authentication.

        Asserts:
        --------
            The response status code is 200.
            The response data contains the updated APIKey's key.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_update = True  # Ensure the update method is allowed

        url = reverse("api-key-detail", kwargs={"pk": apikey.pk})
        data = {"is_active": True}
        response = api_client.patch(url, data, format="json")

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            response.data["is_active"] is True
        ), f"Expected is active with flag 'True', got {response.data['is_active']}"

    def test_destroy_apikey(
        self,
        api_client: APIClient,
        admin_user: User,
        apikey: APIKey,
    ):
        """
        Test the destroy endpoint for APIKey.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            apikey (APIKey): The APIKey instance to delete.

        Asserts:
        --------
            The response status code is 204.
            The APIKey is deleted from the database.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_delete = True  # Ensure the destroy method is allowed

        url = reverse("api-key-detail", kwargs={"pk": apikey.pk})
        response = api_client.delete(url)

        assert (
            response.status_code == 204
        ), f"Expected 204 No Content, got {response.status_code}."
        assert not APIKey.objects.filter(
            pk=apikey.pk
        ).exists(), "APIKey was not deleted"

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

        url = reverse("api-key-list")
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

        url = reverse("api-key-detail", kwargs={"pk": apikey.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_list_apikey_with_has_apikey_permission(
        self,
        api_client: APIClient,
        apikey: APIKey,
    ):
        """
        Test the list endpoint with HasAPIKey Permission as an extra permission.

        Configures the viewset to require HasAPIKey Permission and authenticates
        the request using the API key in the header.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            apikey (APIKey): A sample APIKey instance for authentication and data.

        Asserts:
        --------
            The response status code is 200 when authenticated with the API key.
            The response data contains the expected API key.
            The response status code is 403 when no API key is provided, due to authentication failure.
        """
        # Configure the viewset to allow list and add HasAPIKey
        config.api_allow_list = True
        config.api_extra_permission_class = HasAPIKey

        # Define header settings based on config
        header_name = getattr(config, "header_name", "Authorization")
        header_prefix = getattr(config, "header_type", "Bearer")
        header_value = f"{header_prefix} {apikey.key}" if header_prefix else apikey.key
        header_key = (
            f"HTTP_{header_name.replace('-', '_').upper()}"  # e.g., HTTP_AUTHORIZATION
        )

        # Set the API key header
        api_client.credentials(**{header_key: header_value})

        # Test successful request with API key
        url = reverse("api-key-list")
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK with API key, got {response.status_code} with response: {response.data}"
        assert "results" in response.data, "Expected 'results' in response data."
        assert len(response.data["results"]) > 0, "Expected data in the results."
        assert (
            response.data["results"][0]["key"] == apikey.key
        ), f"Expected API key {apikey.key}, got {response.data['results'][0]['key']}"

        # Test request without API key (should fail due to authentication)
        api_client.credentials()  # Clear credentials
        response = api_client.get(url)

        assert (
            response.status_code == 403
        ), f"Expected 403 Forbidden without API key, got {response.status_code} with response: {response.data}"
        assert "detail" in response.data, "Expected error detail in response."
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        ), f"Expected 'Authentication credentials were not provided.', got {response.data['detail']}"
