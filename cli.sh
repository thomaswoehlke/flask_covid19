#!/usr/bin/env bash

. ./venv/bin/activate

export FLASK_APP=app.py
export FLASK_ENV=development

flask --help
