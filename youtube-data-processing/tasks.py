from celery import Celery
from main import run_processing_job

app = Celery('tasks', broker='redis://redis:6379/0')

@app.task
def processing_task():
    run_processing_job()
