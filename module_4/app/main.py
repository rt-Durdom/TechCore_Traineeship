import time

import asyncio
from fastapi import FastAPI, Request

from app.api.routers import api_router
from app.api.endpoints import reviews
from app.core.invalidator import in_invalidator


app = FastAPI()


@app.event('startup')
async def startup_event():
    asyncio.create_task(in_invalidator.listen_for_invalidation())


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    method = request.method
    url = request.url
    start_time = time.perf_counter()
    result = await call_next(request)
    process_time = time.perf_counter() - start_time
    return result

app.include_router(api_router)
app.include_router(reviews.router)
