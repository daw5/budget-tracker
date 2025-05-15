from django.db import models
from .querysets import CampaignQuerySet

class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_date = models.DateField(auto_now_add=True)
    monthly_budget = models.IntegerField(default = 0)
    daily_budget = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.name

class Campaign(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    created_date = models.DateField(auto_now_add=True)
    active = models.BooleanField()  
    start_hour = models.IntegerField(default = 0)
    end_hour = models.IntegerField(default = 0)
    objects = CampaignQuerySet.as_manager()
    
    def __str__(self):
        return self.name

class DailySpend(models.Model):
    Campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='dailyspends'
    )
    created_date = models.DateField(auto_now_add=True)
    amount_spent = models.IntegerField(default = 0)
    
    def __str__(self):
        return (f'{self.Campaign.name} spend for date {self.created_date}')
    
