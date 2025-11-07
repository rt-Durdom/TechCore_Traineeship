import time

from fastapi import FastAPI, Request

from app.api.routers import api_router

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    method = request.method
    url = request.url
    start_time = time.perf_counter()
    result = await call_next(request)
    process_time = time.perf_counter() - start_time
    return result

app.include_router(api_router)
