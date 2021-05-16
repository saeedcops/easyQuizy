web: daphne app.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: celery -A app worker --beat