from fastapi import APIRouter
from module_4.app_celery.tasks import process_order


cel_router = APIRouter()

@cel_router.post('/order')
async def order(order_id):
    res = process_order.delay(order_id)
    return res.id
