FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

COPY module_4/ ./module_4/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "celery", "-A", "module_4.app_celery.new_app_celery", "worker", "--loglevel=info"]