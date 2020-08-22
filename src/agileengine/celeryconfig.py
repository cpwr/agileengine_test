from celery.schedules import crontab

CELERY_IMPORTS = (
    "tasks.images",
)

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_ENABLE_UTC = True

CELERY_RESULT_BACKEND = "redis://localhost:6379"
CELERY_IGNORE_RESULT = True
BROKER_URL = "redis://localhost:6379"

CELERYBEAT_SCHEDULE = {
    'every-hour': {
        'task': 'tasks.images.cache_images',
        'schedule': crontab(hour="*/1"),
        'options': {'queue': 'images'},
        'args': (1, ),
    },
}