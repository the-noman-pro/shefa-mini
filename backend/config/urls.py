from django.contrib import admin
from django.urls import include, path

from apps.core.views import health

admin.site.site_header = "Shefa mini admin"
admin.site.site_title = "Shefa mini"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health, name="health"),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/wallet/", include("apps.wallets.urls")),
    path("api/", include("apps.cases.urls")),
]
import os
