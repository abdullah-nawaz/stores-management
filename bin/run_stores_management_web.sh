#!/usr/bin/env bash

LOGGING_LEVEL="${LOGGING_LEVEL:DEBUG}"

# run latest migrations
python manage.py deploy

gunicorn --reload --access-logfile "-" --error-logfile "-" --log-level LOGGING_LEVEL --worker-class gevent --workers=3 --timeout 60 --bind 0.0.0.0:8081 manage:app
