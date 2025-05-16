# Pseudo Code

### A brief overview of this application's design:

#### Models:

- A brand has many campaigns. Key fields: daily budget, monthly budget.
- A campaign has many daily spends, up to one per day. Key fields: Active, start hour / end hour (window in which this campaign should be active)
- A daily spend is a daytight compartment. Key fields: created date (every model has created date, but on this model it is a very important field), amount spend (in $)

#### Basic Logic Overview:

##### Tracking spend

All spend data is logged in the DailySpends, so if this app were to be extended in the future, it would be a simple matter to query and display spend per campaign / brand / day / month. We only create a DailySpend if money was spent on that day, avoiding unnecessary empty records.

##### Budget enforcement

There is one api endpoint which increments the DailySpend of a given campaign, for a given brand, on a given day. It checks if Celery has marked that campaign as active or not before creating / updating any DailySpend records, ensuring that no additional money can be spent once Celery has marked that campaign as inactive.

##### Dayparting checks

I was initially going to go with multiple tasks, as the challenge description seemed to suggest that, but upon actually writing the code, I found that a single task which calls multiple functions is more than sufficient, and keeps everything in sync. This task manages active states for campaigns. It first checks if there are any campaigns which are currently deactivated, but are under budget and within their dayparting window, and if any of these campaigns can be activated, they are. It then checks if any are over their monthly budget, their daily budget, or outside of the dayparting window, and deactivates them if so.

##### Daily/monthly resets

I am always looking for the most simple and elegant solution that ensures required functionality, while being iterable, so there is room to expand if the business requests it. Because of the design path I have chosen, there is no need to reset the daily / monthly budget. When the day / month rolls over, my queries will take into account that it is a new day / month, and not include any daily spends from previous months when calculating if we are over budget or not.
