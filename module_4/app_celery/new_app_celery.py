from celery import Celery
from kombu import Queue


celery_app = Celery(
    'worker_celery',
    broker='amqp://guest:guest@localhost:5672//',
    backend='redis://localhost:6379/0',
    include=['module_4.app_celery.tasks']
)

celery_app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_queues=(
        Queue(
            'celery',
            queue_arguments={
                'x-dead-letter-exchange': '',
                'x-dead-letter-routing-key': 'celery_error'
            }
        )
    )
)
