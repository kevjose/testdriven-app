import os
import time
from celery import Celery
import celeryconfig

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery.config_from_object(celeryconfig)
apps = []
for x in next(os.walk('.'))[1]:
    app_str = x
    for y in next(os.walk('./'+str(x)))[1]:
        app_str_final = app_str+'.'+str(y)
        apps.append(app_str_final)





celery.autodiscover_tasks(packages=apps,force=True)

@celery.task(name='tasks.add', bind=True)
def add(self, x: int, y: int) -> int:
    time.sleep(300)
    return x + y