from django.urls import path
from .views import create_or_update_daily_spend

urlpatterns = [
    path('api/update-daily-spend/', create_or_update_daily_spend),
]