from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

app = Celery('tasks',broker= os.getenv('REDIS_URL'))

app.conf.imports = ['tasks']

app.conf.beat_schedule = {
    'call-api-every-two-minutes': {
        'task': 'tasks.cron_blog_writer',
        'schedule': 120.0,
    },
}
