import os
from celery import Celery
import billiard as multiprocessing
from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'say-hello-every-30-seconds': {
        'task': 'loan.tasks.check_applications',
        'schedule': timedelta(seconds=10*60),
        'args': ()
    },
}

# @app.task(bind=True)
# def test_task(self):
#     print(f'Request: {self.request!r}')


if __name__ == '__main__':
    multiprocessing.freeze_support()
