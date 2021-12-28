
set FLASK_APP=app.py
set FLASK_ENV=development

start /max cmd /t:8f /k "celery --app app.celery worker --pool eventlet --loglevel INFO"

start /max cmd /t:90 /k "flask run"
