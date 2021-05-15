release: python manage.py wait_for_db && python manage.py migrate && python manage.py collectstatic --dry-run --noinput
web: daphne app.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: celery -A app worker -B --loglevel=info && python3 manage.py runworker channel_layer -v2