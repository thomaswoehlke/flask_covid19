#!/usr/bin/env bash

. ./venv/bin/activate

celery --app app.celery worker --pool eventlet --loglevel INFO &

export FLASK_APP=app.py
export FLASK_ENV=development

flask run
