web: uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port $PORT
worker: celery -A worker.tasks_missions worker --loglevel=info
beat: celery -A worker.tasks_missions beat --loglevel=info
