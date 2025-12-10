from fastapi import APIRouter

from gateway.app.api.endpoint import router_gateway

api_router_gateway = APIRouter()

api_router_gateway.include_router(
    router_gateway,
    prefix='/api/books',
    tags=['books'],)
