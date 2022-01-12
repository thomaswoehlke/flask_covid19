# flask_covid19

* Version 0.0.87

## git

* [https://github.com/thomaswoehlke/flask_covid19.git](https://github.com/thomaswoehlke/flask_covid19.git)

````bash
    git clone git@github.com:thomaswoehlke/flask_covid19.git
    cd flask_covid19
````

## venv

### prepare venv

````bash
    make venv
    . ./venv/bin/activate
    make start
````

### update dependencies

````bash
    . ./venv/bin/activate
    make update
 ````

## run

### run services web and celery

````bash
    ./mq.sh
````

### run cli tasks

````bash
    . ./venv/bin/activate
    export FLASK_APP=app
    export FLASK_ENV=development
    flask --help
````

## configuration

### change configuration

````bash
    vim project/data/config.py
    vim project/data/database.py
    vim project/data/pytestconfig.py
    vim project/data/requirements_in/build.in
````

### change dependencies

````bash
    . ./venv/bin/activate
    make update
    vim project/data/requirements_in/build.in
    vim project/data/requirements_in/docs.in
    vim project/data/requirements_in/tests.in
    vim project/data/requirements_in/typing.in
    vim project/data/requirements_in/dev.in
    vim project/data/requirements_in/linux.in
    vim project/data/requirements_in/windows.in
    make update
````

## Software Technology

### Python

* [flask](https://flask.palletsprojects.com/en/1.1.x/)
* [flask: pypi](https://pypi.org/project/Flask/)
* [flask: flask-admin](https://github.com/flask-admin/flask-admin/)
* [flask: werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/)
* [flask: sqlalchemy](https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/)
* [sqlalchemy](https://docs.sqlalchemy.org/en/13/)
* [sqlite](https://sqlite.org/docs.html)
* [jinja](https://jinja.palletsprojects.com/en/2.11.x/)
* [jinja: markupsafe](https://palletsprojects.com/p/markupsafe/)
* [jinja: itsdangerous](https://palletsprojects.com/p/itsdangerous/)
* [jinja: click](https://palletsprojects.com/p/click/)

### Info

* [sqlalchemy-query-with-or-and-like-common-filters](http://www.leeladharan.com/sqlalchemy-query-with-or-and-like-common-filters)
* [pagination-route-example-with-flask-sqlalchemy-paginate](https://riptutorial.com/flask/example/22201/pagination-route-example-with-flask-sqlalchemy-paginate)

### Dependencies

* [fixing-conflicting-dependencies](https://pip.pypa.io/en/latest/user_guide/#fixing-conflicting-dependencies)

## Statistical Data and their Sources

* [WHO](https://covid19.who.int/WHO-COVID-19-global-data.csv)
* [ecdc.europa](https://opendata.ecdc.europa.eu/covid19/casedistribution/csv)
* [ecdc.europa - Information](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide)
* [OWID: covid-19-data](https://github.com/owid/covid-19-data)
* [OWID: covid-vaccinations](https://ourworldindata.org/covid-vaccinations)
* [OWID: coronavirus-data-explorer](https://ourworldindata.org/explorers/coronavirus-data-explorer)

## UML

### all

#### all_domain_model

![all_domain_model](uml/data_all/old/all_domain_model.png)

#### all_domain_model_import

![all_domain_model_import](uml/data_all/old/all_domain_model_import.png)

#### all_domain_model_star_schema

![all_domain_model_star_schema](uml/data_all/old/all_domain_model_star_schema.png)

#### all_use_cases

![all_use_cases](uml/data_all/old/all_use_cases.png)

### ecdc

#### ecdc_domain_model

![ecdc_domain_model](uml/data_ecdc/old/ecdc_domain_model.png)

#### ecdc_domain_model_import

![ecdc_domain_model_import](uml/data_ecdc/old/ecdc_domain_model_import.png)

#### ecdc_use_cases

![ecdc_use_cases](uml/data_ecdc/old/ecdc_use_cases.png)

### owid

#### owid_domain_model

![owid_domain_model](uml/data_owid/old/owid_domain_model.png)

#### owid_domain_model_import

![owid_domain_model](uml/data_owid/old/owid_domain_model_import.png)

#### owid_use_cases

![owid_use_cases](uml/data_owid/old/owid_use_cases.png)

#### owid_use_cases_visual_data_1

![owid_report_01](uml/data_owid_reports/owid_report_01.png)

#### owid_use_cases_visual_data_2

![owid_report_02](uml/data_owid_reports/owid_report_02.png)

#### owid_use_cases_visual_data_3

![owid_report_03](uml/data_owid_reports/owid_report_03.png)

#### owid_use_cases_visual_data_4

![owid_report_04](uml/data_owid_reports/owid_report_04.png)

#### owid_use_cases_visual_data_5

![owid_report_05](uml/data_owid_reports/owid_report_05.png)

#### owid_use_cases_visual_data_5

![owid_report_06](uml/data_owid_reports/owid_report_06.png)

#### owid_use_cases_visual_data_5

![owid_report_07](uml/data_owid_reports/owid_report_07.png)

#### owid_report_08

![owid_report_08](uml/data_owid_reports/owid_report_08.png)

#### owid_report_09

![owid_report_09](uml/data_owid_reports/owid_report_09.png)

#### owid_report_10

![owid_report_10](uml/data_owid_reports/owid_report_10.png)

### rki_vaccination

#### rki_vaccination_domain_model

![rki_vaccination_domain_model](uml/data_vaccination/old/rki_vaccination_domain_model.png)

#### rki_vaccination_domain_model_import

![rki_vaccination_domain_model](uml/data_vaccination/old/rki_vaccination_domain_model.png)

#### rki_vaccination_use_cases

![rki_vaccination_use_cases](uml/data_vaccination/old/rki_vaccination_use_cases.png)

### who

#### who_domain_model

![rki_vaccination_use_cases](uml/data_vaccination/old/rki_vaccination_use_cases.png)

#### who_domain_model_import

![who_domain_model_import](uml/data_who/old/who_domain_model_import.png)

#### who_use_cases

![who_use_cases](uml/data_who/old/who_use_cases.png)

### app_web

#### app_web_domain_model

![app_application_domain_model](uml/app_web/old/app_application_domain_model.png)

#### app_web_use_cases

![app_application_use_cases](uml/app_web/old/app_application_use_cases.png)
