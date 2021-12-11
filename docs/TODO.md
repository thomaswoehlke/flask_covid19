# TODO

## Jinja

* https://jinja.palletsprojects.com/en/2.11.x/templates/

## Celery

* https://stackabuse.com/asynchronous-tasks-using-flask-redis-and-celery/
* https://docs.celeryproject.org/en/stable/userguide/monitoring.html#monitoring-redis-queues
* https://docs.celeryproject.org/en/stable/userguide/daemonizing.html#service-file-celery-service

### Setuptools

* https://setuptools.readthedocs.io/en/latest/userguide/dependency_management.html#python-requirement
* https://setuptools.readthedocs.io/en/latest/userguide/dependency_management.html
* https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html
* https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html#basic-use

### Flask-Login

* https://flask-login.readthedocs.io/en/latest/
* https://riptutorial.com/flask/example/28112/using-flask-login-extension

### blueprints

* https://flask.palletsprojects.com/en/1.1.x/blueprints/

### Bootstrap Theme

* https://startbootstrap.com/template/sb-admin-angular
* https://github.com/startbootstrap/sb-admin-angular
* https://startbootstrap.com/previews/sb-admin-angular

### Visual Studio Code

* Flask Tutorial in Visual Studio Code: https://code.visualstudio.com/docs/python/tutorial-flask

### packaging

* https://packaging.python.org/

### 0.0.17 Release

* Fixed #123 split RkiBundeslaenderService into two Services, one for bundeslaender and one for landkreise
* Fixed #128 add fields from csv to RkiLandkreiseImport
* Fixed #139 refactor RkiBundeslaenderServiceDownload to new method scheme introduced 07.02.2021
* Fixed #140 move OwidImport to RKI in: rk_service_import.py
* Fixed #125 implement RkiLandkreise
* Fixed #126 implement RkiBundeslaenderImport

### 0.0.18 Release

* Fixed #39 SQLalchemy instead of SQL: AllModelClasses.remove_all()
* Fixed #40 SQLalchemy instead of SQL: EcdcImport.get_date_rep()
* Fixed #41 SQLalchemy instead of SQL: EcdcImport.get_countries_of_continent()
* Fixed #107 SQLalchemy instead of SQL in: EcdcImport.get_countries_of_continent
* Fixed #109 SQLalchemy instead of SQL in: EcdcImport.get_date_rep
* Fixed #110 SQLalchemy instead of SQL in: EcdcImport.get_continent

### Research

* add [Flask-Caching](https://pypi.org/project/Flask-Caching/)
* add [Flask-Monitoring](https://pypi.org/project/Flask-Monitoring/)
* add [Flask-Redisboard](https://pypi.org/project/Flask-Redisboard/)
* add [Flask-Babel](https://pypi.org/project/Flask-Babel/)
* add [flask-resources](https://pypi.org/project/flask-resources/)
* add [flask-whooshalchemy3](https://pypi.org/project/flask-whooshalchemy3/)
* add [flask-whooshalchemy3 (github)](https://github.com/blakev/Flask-WhooshAlchemy3)
* add [flask-filealchemy](https://pypi.org/project/flask-filealchemy/)

### mariadb and sqlalchemy

* https://stackoverflow.com/questions/12273889/calculate-execution-time-for-every-page-in-pythons-flask
* https://docs.sqlalchemy.org/en/13/faq/performance.html
* https://mariadb.com/kb/en/query-cache/
* https://docs.sqlalchemy.org/en/14/core/pooling.html
* https://docs.sqlalchemy.org/en/14/core/pooling.html?highlight=disconnects#dealing-with-disconnects
* https://mariadb-corporation.github.io/mariadb-connector-python/
* https://mariadb.com/docs/clients/connector-python/
* https://jinja.palletsprojects.com/en/2.11.x/templates/

### git setup

* https://git-scm.com/book/en/v2/Git-Tools-Submodules

````bash
        git submodule init
        git submodule update
        git config --global diff.submodule log

        git submodule update --remote --merge
````

### yo

* https://flask-caching.readthedocs.io/en/latest/
* https://www.howtoforge.de/anleitung/wie-installiere-ich-memcached-auf-ubuntu-2004-lts/

## Testing
* https://testdriven.io/blog/flask-pytest/
* https://docs.pytest.org/en/latest/
* https://flask.palletsprojects.com/en/2.0.x/testing/
* https://pytest-flask.readthedocs.io/en/latest/index.html
