import json

from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from budgettracker.types import SpendRequest
from .models import Campaign, DailySpend
from django.utils import timezone

@csrf_exempt
def create_or_update_daily_spend(request: HttpRequest) -> JsonResponse | HttpResponseBadRequest:
    try:
        data: SpendRequest = json.loads(request.body)
        campaign_name: str | None = data.get('name')
        amount_spent: int | None = data.get('amount')

        if not campaign_name or not amount_spent:
            return JsonResponse({'error': 'Missing required fields (name and amount).'}, status=400)
        
        campaign: Campaign = Campaign.objects.get(name=campaign_name)
        
        if not campaign.active:
            return JsonResponse({'error': 'Campaign is inactive.'}, status=400)

        today: date = timezone.now().date()

        daily_spend, _ = DailySpend.objects.get_or_create(
            campaign=campaign,
            created_date=today
        )

        updated_amount_spent: int = daily_spend.amount_spent + amount_spent

        daily_spend.amount_spent = updated_amount_spent
        daily_spend.save()
        
        return JsonResponse({
            'Amount spent on this day': updated_amount_spent,
        })

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")