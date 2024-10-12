# celery_app.py

from celery import Celery
from config import Config

celery = Celery(
    'app',
    broker=Config.broker_url,
    backend=Config.result_backend,
    include=Config.include
)

celery.conf.update(
    result_expires=3600,
    worker_pool='solo',  # Set the concurrency pool to solo
)

if __name__ == '__main__':
    celery.start()
