# flask_covid19
* Version 0.0.65

## git
* github: https://github.com/thomaswoehlke/flask_covid19.git

## Data Sources:
* [WHO](https://covid19.who.int/WHO-COVID-19-global-data.csv)
* [ecdc.europa](https://opendata.ecdc.europa.eu/covid19/casedistribution/csv)
* [ecdc.europa - Information](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide)

## Python
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
* http://www.leeladharan.com/sqlalchemy-query-with-or-and-like-common-filters
* https://riptutorial.com/flask/example/22201/pagination-route-example-with-flask-sqlalchemy-paginate

### Dependencies
* https://pip.pypa.io/en/latest/user_guide/#fixing-conflicting-dependencies

## UML Blueprints

### all
#### all_domain_model
![all_domain_model](blueprints/data_all/uml/img/all_domain_model.png)
#### all_domain_model_import
![all_domain_model_import](blueprints/data_all/uml/img/all_domain_model_import.png)
#### all_domain_model_import
![all_domain_model_import](blueprints/data_all/uml/img/all_domain_model_star_schema.png)
#### all_use_cases
![all_use_cases](blueprints/data_all/uml/img/all_use_cases.png)

### ecdc
#### ecdc_domain_model
![ecdc_domain_model](blueprints/data_ecdc/uml/img/ecdc_domain_model.png)
#### ecdc_domain_model_import
![ecdc_domain_model_import](blueprints/data_ecdc/uml/img/ecdc_domain_model_import.png)
#### ecdc_use_cases
![ecdc_use_cases](blueprints/data_ecdc/uml/img/ecdc_use_cases.png)

### owid
#### owid_domain_model
![owid_domain_model](blueprints/data_owid/uml/img/owid_domain_model.png)
#### owid_domain_model_import
![owid_domain_model](blueprints/data_owid/uml/img/owid_domain_model_import.png)
#### owid_use_cases
![owid_use_cases](blueprints/data_owid/uml/img/owid_use_cases.png)
#### owid_use_cases_visual_data_1
![owid_use_cases_visual_data_1](blueprints/data_owid/uml/use_cases__visual_data/img/owid_use_cases_visual_data_1.png)
#### owid_use_cases_visual_data_2
![owid_use_cases_visual_data_2](blueprints/data_owid/uml/use_cases__visual_data/img/owid_use_cases_visual_data_2.png)
#### owid_use_cases_visual_data_3
![owid_use_cases_visual_data_3](blueprints/data_owid/uml/use_cases__visual_data/img/owid_use_cases_visual_data_3.png)
#### owid_use_cases_visual_data_4
![owid_use_cases_visual_data_4](blueprints/data_owid/uml/use_cases__visual_data/img/owid_use_cases_visual_data_4.png)
#### owid_use_cases_visual_data_5
![owid_use_cases_visual_data_5](blueprints/data_owid/uml/use_cases__visual_data/img/owid_use_cases_visual_data_5.png)

### rki_vaccination
#### rki_vaccination_domain_model
![rki_vaccination_domain_model](blueprints/data_vaccination/uml/img/rki_vaccination_domain_model.png)
#### rki_vaccination_domain_model_import
![rki_vaccination_domain_model_import](blueprints/data_vaccination/uml/img/rki_vaccination_domain_model.png)
#### rki_vaccination_use_cases
![rki_vaccination_use_cases](blueprints/data_vaccination/uml/img/rki_vaccination_use_cases.png)

### who
#### who_domain_model
![who_domain_model](blueprints/data_vaccination/uml/img/rki_vaccination_use_cases.png)
#### who_domain_model_import
![who_domain_model_import](blueprints/data_who/uml/img/who_domain_model_import.png)
#### who_use_cases
![who_use_cases](blueprints/data_who/uml/img/who_use_cases.png)

### app_web
#### app_web_domain_model
![app_web_domain_model](blueprints/app_web/uml/img/app_application_domain_model.png)
#### app_web_use_cases
![app_web_use_cases](blueprints/app_web/uml/img/app_application_use_cases.png)