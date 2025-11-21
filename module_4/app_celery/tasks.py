import time

from .new_app_celery import celery_app


@celery_app.task(bind=True, max_retries=3, name='module_4.app_celery.process_order')
def process_order(self, order_id):
    try:
        print(f'Получаем заказ:{order_id}')
        # time.sleep(10)
        return order_id
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)
