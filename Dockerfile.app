FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


FROM python:3.12-slim AS final

ENV PATH="/opt/venv/bin:$PATH" PYTHONPATH=/app

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

COPY module_4/__init__.py ./module_4/

COPY module_4/app ./module_4/app

COPY module_4/app_kafka ./module_4/app_kafka

COPY module_4/app_celery ./module_4/app_celery

COPY alembic.ini ./
COPY alembic ./alembic

EXPOSE 8000

CMD ["uvicorn", "module_4.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
