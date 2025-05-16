from celery import shared_task
from .models import Campaign
from django.utils.timezone import now
from django.db.models import Q, F

current_hour = now().hour

@shared_task
def manage_campaign_active_status_for_daily_budget():
    Campaign.objects.under_daily_budget().update(active=True)
    Campaign.objects.over_daily_budget().update(active=False)

    return f'Managing active state for campaigns based on daily budget, current hour: {current_hour}'

@shared_task
def manage_campaign_active_status_for_monthly_budget():
    Campaign.objects.over_monthly_budget().update(active=False)
    Campaign.objects.under_monthly_budget().update(active=True)
    
    return f'Managing active state for campaigns based on monthly budget, current hour: {current_hour}'
    
@shared_task
def manage_campaign_active_status_for_dayparting_window():
    reactivate_inactive_campaigns_within_allowed_window()
    deactivate_active_campaigns_outside_of_allowed_window()
    
    return f'Managing active state for campaigns based on dayparting window, current hour: {current_hour}'

def reactivate_inactive_campaigns_within_allowed_window():
    Campaign.objects.filter(
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
    ).update(active=True)
    
def deactivate_active_campaigns_outside_of_allowed_window():
    Campaign.objects.filter(
        Q(active=True) &
        Q(start_hour__lte=F('end_hour')) & 
            (Q(start_hour__gt=current_hour) | Q(end_hour__lte=current_hour)
        ) |
        Q(start_hour__gt=F('end_hour')) & 
            (Q(start_hour__gt=current_hour) & Q(end_hour__lte=current_hour)
        )
    ).update(active=False)
    
