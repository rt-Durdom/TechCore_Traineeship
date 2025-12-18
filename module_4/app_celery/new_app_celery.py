from celery import Celery
from kombu import Queue
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from module_4.app.core.opentel_config import zipkin_sevice

zipkin_sevice(service_name="celery-worker", zipkin_endpoint="http://zipkin:9411/api/v2/spans")

celery_app = Celery(
    'worker_celery',
    broker='amqp://guest:guest@rabbitmq:5672//',
    backend='redis://redis_db:6379/0',
    include=['module_4.app_celery.tasks',
             'module_4.app_celery.beat_tasks']
)

CeleryInstrumentor().instrument()

celery_app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_queues=(
        Queue(
            'celery',
            queue_arguments={
                'x-dead-letter-exchange': 'celery_error',
                'x-dead-letter-routing-key': 'celery_error'
            }
        ),
    )
)
celery_app.conf.beat_schedule = {
        'nightly_report': {
            'task': 'module_4.app_celery.beat_tasks.nightly_report',
            'schedule': 300.0
        }
    }
