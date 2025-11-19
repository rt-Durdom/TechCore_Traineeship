import time

from .new_app_celery import celery_app


@celery_app.task
def process_order(order_id):
    time.sleep(10)
    return order_id


res = process_order.delay(1)

print(res)