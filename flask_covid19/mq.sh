#!/usr/bin/env bash

celery --app app.celery worker --pool eventlet --loglevel INFO
