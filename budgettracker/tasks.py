from celery import shared_task
from .models import Campaign
from django.utils.timezone import now
from django.db.models import Q, F

@shared_task
def manage_campaign_active_state() -> str:
    current_hour: int = now().hour
    reactivate_campaign_if_possible(current_hour)
    deactivate_campaign_if_necessary(current_hour)
    
    return f'Managing active state for campaigns; current hour: {current_hour}'

def reactivate_campaign_if_possible(current_hour: int) -> None:
    Campaign.objects.filter(within_dayparting_window(current_hour)) \
        .under_all_budgets() \
        .update(active=True)

def deactivate_campaign_if_necessary(current_hour: int) -> None:
    Campaign.objects.over_daily_budget().update(active=False)
    Campaign.objects.over_monthly_budget().update(active=False)
    Campaign.objects.filter(outside_of_dayparting_window(current_hour)).update(active=False)
    
def within_dayparting_window(current_hour: int) -> Q:
    return (
        Q(active=False) &
        (
            Q(start_hour__lte=F('end_hour')) &
            Q(start_hour__lte=current_hour) &
            Q(end_hour__gt=current_hour)
        ) |
        (
            Q(start_hour__gt=F('end_hour')) &
            (Q(start_hour__lte=current_hour) | Q(end_hour__gt=current_hour))
        )
    )
    
def outside_of_dayparting_window(current_hour: int) -> Q:
    return (
        Q(active=True) &
        Q(start_hour__lte=F('end_hour')) & 
            (Q(start_hour__gt=current_hour) | Q(end_hour__lte=current_hour)
        ) |
        Q(start_hour__gt=F('end_hour')) & 
            (Q(start_hour__gt=current_hour) & Q(end_hour__lte=current_hour)
        )
    )
    
