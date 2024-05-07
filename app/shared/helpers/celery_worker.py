from celery import Celery
import time

# Configure Celery
celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)

@celery.task
def upload_simulate_file():
    time.sleep(5)

    print("File uploaded successfully.")
    return




