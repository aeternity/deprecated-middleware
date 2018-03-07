#!/bin/bash

TIMEOUT=120

python manage.py migrate                  # Apply database migrations
#python manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
touch /srv/logs/error.log
tail -n 0 -f /srv/logs/*.log &

/code/docker/wait-for-it.sh -t 120 postgres:5432 -- echo "Postgres is online"
/code/docker/wait-for-it.sh -t 120 redis:6379 -- echo "Redis is online"
/code/docker/wait-for-it.sh -t 120 epoch:3013 -- echo "Epoch is online"

# Start Gunicorn processes
echo Starting Gunicorn.
#python manage.py runserver
exec gunicorn aepp_middleware.wsgi:application \
    --name baeppo \
    --bind 0.0.0.0:8000 \
    --workers 10 \
    --log-level=info \
    --timeout $TIMEOUT \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log \
    --error-logfile=/srv/logs/error.log \
    "$@"
