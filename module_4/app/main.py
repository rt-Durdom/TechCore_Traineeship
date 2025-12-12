import time

import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import Response
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from module_4.app.api.routers import api_router
from module_4.app.api.endpoints import reviews
from module_4.app.core.invalidator import in_invalidator
#from module_4.app_kafka.consumer import consumer
from module_4.app.core.opentel_config import zipkin_sevice


zipkin_sevice(service_name="book-service", zipkin_endpoint="http://zipkin:9411/api/v2/spans")
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()


@app.on_event('startup')
async def startup_event():
    asyncio.create_task(in_invalidator.listen_for_invalidation())

@app.on_event('startup')
async def startup_event2():
    #await asyncio.to_thread(consumer.start_consume_loop())
    pass



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
@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
