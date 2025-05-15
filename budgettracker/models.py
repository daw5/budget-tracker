from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=50)
    created_date = models.DateField(auto_now_add=True)
    monthly_budget = models.IntegerField(default = 0)
    daily_budget = models.IntegerField(default = 0)

    @property
    def total_monthly_spend(self):
        today = timezone.now().date()
        return self.campaigns.filter(
            created__month=today.month,
            created__year=today.year
        ).aggregate(total=Sum('total_monthly_spend'))['total'] or 0

    @property
    def total_daily_spend(self):
        today = timezone.now().date().month
        return self.campaigns.filter(
            created__day=today.day,
            created__month=today.month,
            created__year=today.year
        ).aggregate(total=Sum('total_daily_spend'))['total'] or 0

class Campaign(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_date = models.DateField(auto_now_add=True)
    active = models.BooleanField()  
    start_hour = models.IntegerField(default = 0)
    end_hour = models.IntegerField(default = 0)

    @property
    def total_monthly_spend(self):
        today = timezone.now().date()
        return self.dailyspends.filter(
            created__month=today.month,
            created__year=today.year
        ).aggregate(total=Sum('amount_spent'))['total'] or 0

    @property
    def total_daily_spend(self):
        today = timezone.now().date().month
        return self.dailyspends.filter(
            created__day=today.day,
            created__month=today.month,
            created__year=today.year
        ).aggregate(total=Sum('amount_spent'))['total'] or 0

class DailySpend(models.Model):
    Campaign = models.ForeignKey(Brand, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    amount_spent = models.IntegerField(default = 0)
    
