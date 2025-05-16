import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from .models import Campaign, DailySpend
from django.utils import timezone

@csrf_exempt
def create_or_update_daily_spend(request):
    try:
        data = json.loads(request.body)
        campaign_name = data.get('name')
        amount_spent = data.get('amount')

        if not campaign_name or not amount_spent:
            return JsonResponse({'error': 'Missing required fields (name and amount).'}, status=400)
        
        campaign = Campaign.objects.get(name=campaign_name)

        if not campaign.active:
            return JsonResponse({'error': 'Campaign is inactive.'}, status=400)

        today = timezone.now().date()

        daily_spend, _ = DailySpend.objects.get_or_create(
            campaign=campaign,
            created_date=today
        )

        updated_amount_spent = daily_spend.amount_spent + amount_spent

        daily_spend.amount_spent = updated_amount_spent
        daily_spend.save()
        
        return JsonResponse({
            'Amount spent on this day': updated_amount_spent,
        })

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")