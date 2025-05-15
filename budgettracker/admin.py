from django.contrib import admin

from .models import Brand, Campaign, DailySpend

admin.site.register(Brand)
admin.site.register(Campaign)
admin.site.register(DailySpend)