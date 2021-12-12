rem .\venv\Scripts\activate

start /max cmd /k "celery --app app.celery worker --pool eventlet --loglevel INFO"

set FLASK_APP=app.py
set FLASK_ENV=development

flask run
