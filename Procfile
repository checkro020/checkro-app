web: uvicorn main:app --host 0.0.0.0 --port $PORT
worker: celery -A app.tasks.tasks.celery_app worker --loglevel=info
