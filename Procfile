web: gunicorn manage:app --log-file -
celeryd: celery -A tasks.celery worker --loglevel=info -E
