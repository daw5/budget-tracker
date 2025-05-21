from typing import List
from django.urls import URLPattern, path
from .views import create_or_update_daily_spend

urlpatterns: List[URLPattern] = [
    path('api/update-daily-spend/', create_or_update_daily_spend),
]