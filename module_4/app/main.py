import time

from fastapi import FastAPI, Request

from .api.routers import api_router

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    method = request.method
    url = request.url
    start_time = time.perf_counter()
    await call_next(request)
    process_time = time.perf_counter() - start_time
    return f'Информация о запросе: {method}, {url}, {process_time}'

app.include_router(api_router)
