import os

from django.conf import settings

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogg.settings')

app = Celery('blogg')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')



from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'create-blog-post-every-day': {
        'task': 'your_app_name.tasks.create_daily_blog_post',
        'schedule': crontab(hour=0, minute=0),
    },
}
