from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('apikey_auth/', include("apikey_auth.urls")),
]
