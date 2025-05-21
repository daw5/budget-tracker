from typing import List
from django.contrib import admin
from django.urls import URLResolver, include, path

urlpatterns: List[URLResolver] = [
    path("budgettracker/", include("budgettracker.urls")),
    path("admin/", admin.site.urls),
]