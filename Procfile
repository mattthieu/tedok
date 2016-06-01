web: python manage.py migrate auth && python manage.py migrate && gunicorn tedok.wsgi --log-file -
worker: python manage.py celery worker -B -l info
