# saas/utils/create_periodic_tasks.py
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from saas.tasks import print_hello

def create_periodic_task():
    # Create or get an interval schedule for every 1 minute
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,  # Run every 1 minute
        period=IntervalSchedule.MINUTES,  # Period is in minutes
    )

    # Create or update the periodic task
    PeriodicTask.objects.get_or_create(
        interval=schedule,  # Link the schedule
        name='Print Hello Task',  # Name of the task
        task='saas.tasks.print_hello',  # Full path to the task
    )
