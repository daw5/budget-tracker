from datetime import date
from django.db.models import Sum, F, Q, Value
from django.db.models.functions import Coalesce
from django.utils import timezone
from .models import models

class CampaignQuerySet(models.QuerySet):
    def with_monthly_spend(self):
        today: date = timezone.now().date()
        return self.annotate(
            monthly_spend=Sum(
                'dailyspends__amount_spent',
                filter=Q(
                    dailyspends__created_date__year=today.year,
                    dailyspends__created_date__month=today.month
                )
            )
        )
        
    def with_daily_spend(self):
        today: date = timezone.now().date()
        return self.annotate(
            daily_spend=Sum(
                'dailyspends__amount_spent',
                filter=Q(
                    dailyspends__created_date=today
                )
            )
        )
        
    def with_spends(self):
        today: date = timezone.now().date()
        return self.annotate(
            daily_spend=Coalesce(
                Sum(
                    'dailyspends__amount_spent',
                    filter=Q(
                        dailyspends__created_date=today
                    )
                ),
                Value(0)
            ),
            monthly_spend=Coalesce(
                Sum(
                    'dailyspends__amount_spent',
                    filter=Q(
                        dailyspends__created_date__year=today.year,
                        dailyspends__created_date__month=today.month
                    )
                ),
                Value(0)
            )
        )
    
    def under_all_budgets(self):
        return self.with_spends().filter(
            daily_spend__lte=F('brand__daily_budget'),
            monthly_spend__lte=F('brand__monthly_budget')
        )

    def over_monthly_budget(self):
        return self.with_monthly_spend().filter(
            monthly_spend__gt=F('brand__monthly_budget')
        )

    def over_daily_budget(self):
        return self.with_daily_spend().filter(
            daily_spend__gt=F('brand__daily_budget')
        )