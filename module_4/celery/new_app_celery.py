from celery import Celery


celery_app = Celery(
    'worker_celery',
    broker='amqp://guest:guest@localhost:5672//',
    backend='redis://localhost:6379/0',
    include=['tasks']
)