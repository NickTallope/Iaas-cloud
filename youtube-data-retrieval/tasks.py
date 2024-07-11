from celery import Celery
from main import run_retrieval_job

app = Celery('tasks', broker='redis://redis:6379/0')

@app.task
def retrieval_task():
    run_retrieval_job()
