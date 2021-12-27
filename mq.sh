#!/usr/bin/env bash

. ./venv/bin/activate

export FLASK_APP=app
export FLASK_ENV=development

celery --app app.celery worker --pool eventlet --loglevel INFO &

flask run  --host=0.0.0.0 --port=9090
