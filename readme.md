# Budget Tracker

### A simple budget tracking app built using django and celery

## Instructions to run:

Please ensure you have docker running.

From the root of this repository, run the following commands:

```
docker compose build
docker compose up -d
docker-compose run app python manage.py createsuperuser
```

Follow the prompts to finish creating your user (we will need these credentials in order to access the django admin panel)

No more setup necessary, we're done! You can visit the admin panel at http://localhost:8000/admin/ and log in with the user you just created.

## Using the app

As you will see upon logging into the admin panel, some seed data has been created. We have two brands, each with two campaigns. I have given them arbitrary parameters for dayparting, so depending on what time of day it is, these campaigns will either be active or inactive (by default they are all active, but once we ran docker compose, the celery tasks began to run, so it is likely some of these campaigns will be inactive by the time you view them).

Before proceeding to the next step, ensure that at least one campaign is active, and that it's dayparting parameters don't exclude the current time (I have set the timezone to 'America/Los_Angeles', for a production application this would be an env variable in an uncommitted file, but for ease of setup / testing we are hardcoding it)

To spend some money on ads, run the following command in your terminal:

```
curl -X POST http://127.0.0.1:8000/budgettracker/api/update-daily-spend/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Classic Coke", "amount": 1}'
```

This buys one dollar's worth of ads for the 'Classic Coke' campaign. Returned will be the total amount spent on this day. Run it a second time to see the number increment.

To test that Celery is keeping everything within Coke's budget, try adding a larger amount. I have defaulted Coke's daily budget to 1000, and the Celery task which adjusts a campaign's active state based on daily budget runs every 10 seconds. Add an amount which exceeds Coke's daily budget and within 10 seconds, the campaign will have been deactivated, and no more money can be spent!

Feel free to play around with adjusting parameters manually in the django admin panel, and watch how Celery reacts to active / deactivate campaigns!

## Type Checking

Run the below command from the root of the project in order to perform static type checking:

```
mypy .
```
