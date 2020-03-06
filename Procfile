web: gunicorn planeks.wsgi --log-file -
worker: celery worker -A planeks -E -l debug