from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("budgettracker/", include("budgettracker.urls")),
    path("admin/", admin.site.urls),
]