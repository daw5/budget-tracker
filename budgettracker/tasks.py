from celery import shared_task
from .models import Campaign, DailySpend, Brand

# 1. Creating a task which, once every minute, looks at each brand in the database and determines whether or not it is over budget or the day / month, and if so, set active = false for all of that brand’s campaigns
# 2. Have another task, which, once every minute, checks each campaign to see if it is within the dayparting window or not. If not, and campaign is active, set to false. If it is inactive, and within dayparting window, set to true. 
# 3. These first two tasks can probably be one task calling two functions, since we are pulling the same data and writing to the same model. 
# 4. Have a third task which only runs when the day turns over, and re activates the campaign if monthly budget is not yet exceeded and it is inactive (because it went over the day before, or the month before). 

@shared_task
def manage_campaign_active_state():
    Campaign.objects.over_monthly_budget().update(active=False)
    Campaign.objects.over_daily_budget().update(active=False)

    return f"don call me bambooooner"