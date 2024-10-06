from celery import Celery

app = Celery('tasks', broker='redis://:5pSsfS3zgZxASDWkIfVuFcOcUsjtrRCU@redis-16584.c264.ap-south-1-1.ec2.redns.redis-cloud.com:16584/0')

app.conf.imports = ['tasks']

app.conf.beat_schedule = {
    'call-api-every-two-minutes': {
        'task': 'tasks.call_api',
        'schedule': 30.0,
    },
}
