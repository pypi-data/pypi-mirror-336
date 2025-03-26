from django.urls import path
from rest_framework.routers import DefaultRouter

from apikey_auth.api.views import AdminAPIKeyViewSet, APIKeyViewSet
from apikey_auth.views import APIKeyListView

router = DefaultRouter()
router.register("apikey", AdminAPIKeyViewSet, basename="api-key")
router.register("my-apikey", APIKeyViewSet, basename="my-api-key")

urlpatterns = [
    path("api_keys/", APIKeyListView.as_view(), name="api_keys"),
]

urlpatterns += router.urls
