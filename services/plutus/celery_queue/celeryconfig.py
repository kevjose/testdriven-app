from celery.schedules import crontab

# CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'tasks-celery': {
        'task': 'tasks.add',
        'schedule': crontab(minute="*/10"),
        'args': (26, 16)
    }
}