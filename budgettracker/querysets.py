from django.db.models import Sum, F, Q
from django.utils import timezone
from .models import models

class CampaignQuerySet(models.QuerySet):
    def with_monthly_spend(self):
        today = timezone.now().date()
        return self.annotate(
            monthly_spend=Sum(
                'dailyspends__amount_spent',
                filter=Q(
                    dailyspends__created_date__year=today.year,
                    dailyspends__created_date__month=today.month
                )
            )
        )

    def over_monthly_budget(self):
        return self.with_monthly_spend().filter(
            monthly_spend__gt=F('brand__monthly_budget')
        )
    
    def with_daily_spend(self):
        today = timezone.now().date()
        return self.annotate(
            daily_spend=Sum(
                'dailyspends__amount_spent',
                filter=Q(
                    dailyspends__created_date=today
                )
            )
        )

    def over_daily_budget(self):
        return self.with_daily_spend().filter(
            daily_spend__gt=F('brand__daily_budget')
        )