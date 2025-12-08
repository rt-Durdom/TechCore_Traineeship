from fastapi import FastAPI

from gateway.app.routers import api_router_gateway

app = FastAPI(title="API Gateway")

app.include_router(api_router_gateway)
