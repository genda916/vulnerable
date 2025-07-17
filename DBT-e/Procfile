web: gunicorn 'main:create_app()'
worker: celery -A tasks.celery worker --loglevel=info
