from celery import Celery
from celery.schedules import crontab

app = Celery('youtube_pipeline', broker='redis://redis:6379/0')
app.conf.beat_schedule = {
    'run-retrieval-job-at-6pm': {
        'task': 'tasks.retrieval_task',
        'schedule': crontab(hour=12, minute=25),
    },
    'run-processing-job-at-630pm': {
        'task': 'tasks.processing_task',
        'schedule': crontab(hour=12, minute=30),
    },
}