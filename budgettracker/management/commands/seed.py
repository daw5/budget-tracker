from django.core.management.base import BaseCommand
from budgettracker.models import Brand, Campaign

class Command(BaseCommand):
    help = 'Seeding brands and campaigns'

    def handle(self, *args, **kwargs):
        Brand.objects.all().delete()
        Campaign.objects.all().delete()

        coke = Brand.objects.create(name='Coca-Cola', daily_budget=1000, monthly_budget=15000)
        pepsi = Brand.objects.create(name='Pepsi', daily_budget=500, monthly_budget=11000)

        Campaign.objects.create(
            brand=coke,
            name="Classic",
            start_hour=6,
            end_hour=20,
            active=True,
        )

        Campaign.objects.create(
            brand=coke,
            name="Diet",
            start_hour=0,
            end_hour=24,
            active=True,
        )

        Campaign.objects.create(
            brand=pepsi,
            name="Classic",
            start_hour=6,
            end_hour=18,
            active=True,
        )

        Campaign.objects.create(
            brand=pepsi,
            name="Diet",
            start_hour=6,
            end_hour=24,
            active=True,
        )

        self.stdout.write(self.style.SUCCESS("Brands and campaigns seeded"))