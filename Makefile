TZ := 'Europe/Berlin'
HEUTE := `date '+%Y_%m_%d'`

DATA_DIR := flask_covid19/data
DB_DIR := flask_covid19/db
PYTHON := python
PIP_COMPILE := pip-compile
PIP := pip
NPM := npm
PIP_REQUIREMENTS_DIR := flask_covid19/flask_covid19_build/requirements


WHO_URL := https://covid19.who.int/WHO-COVID-19-global-data.csv
WHO_FILE_BACKUP := WHO_backup.csv
WHO_FILE := WHO.csv
WHO_LOG := WHO.csv.log
WHO_SUBDIR := $(DATA_DIR)/who

OWID_URL := https://covid.ourworldindata.org/data/owid-covid-data.csv
OWID_FILE_BACKUP := OWID_backup.csv
OWID_FILE := OWID.csv
OWID_LOG := OWID.csv.log
OWID_SUBDIR := $(DATA_DIR)/owid

RKI_URL := https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data
RKI_FILE_BACKUP := RKI_backup.csv
RKI_FILE := RKI.csv
RKI_LOG := RKI.csv.log
RKI_SUBDIR := $(DATA_DIR)/rki

RKI_VACCINATION_URL := https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv
RKI_VACCINATION_FILE_BACKUP := Vaccination_backup.tsv
RKI_VACCINATION_FILE := Vaccination.tsv
RKI_VACCINATION_LOG := Vaccination.tsv.log
RKI_VACCINATION_SUBDIR := $(DATA_DIR)/vaccination

DIVI_URL := https://www.intensivregister.de/api/public/intensivregister
DIVI_FILE_BACKUP := DIVI_backup.json
DIVI_FILE := DIVI.json
DIVI_LOG := DIVI.json.log
DIVI_SUBDIR := $(DATA_DIR)/divi

ECDC_URL := https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/
ECDC_FILE_BACKUP := ECDC_backup.csv
ECDC_FILE := ECDC.csv
ECDC_LOG := ECDC.csv.log
ECDC_SUBDIR := $(DATA_DIR)/ecdc

.PHONY: all

all: clean start


# -----------------------------------------------------------------------------------------------------
#
#    clean
#
# -----------------------------------------------------------------------------------------------------

clean:
	@echo "clean"
	rm -rf .eggs
	rm -rf artefact_content.egg-info
	rm -rf build
	rm -rf dist
	rm -rf .checkmate
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

# -----------------------------------------------------------------------------------------------------
#
#    pip
#
# -----------------------------------------------------------------------------------------------------

pip_check:
	@echo "pip_check"
	$(PYTHON) -m pip check

pip_compile:
	@echo "pip_compile"
	$(PIP_COMPILE) -r $(PIP_REQUIREMENTS_DIR)/build.in
	$(PIP_COMPILE) -r $(PIP_REQUIREMENTS_DIR)/docs.in
	$(PIP_COMPILE) -r $(PIP_REQUIREMENTS_DIR)/tests.in
	$(PIP_COMPILE) -r $(PIP_REQUIREMENTS_DIR)/dev.in

pip_install:
	@echo "pip_install"
	$(PIP) install -r $(PIP_REQUIREMENTS_DIR)/build.txt
	$(PIP) install -r $(PIP_REQUIREMENTS_DIR)/docs.txt
	$(PIP) install -r $(PIP_REQUIREMENTS_DIR)/tests.txt
	$(PIP) install -r $(PIP_REQUIREMENTS_DIR)/dev.txt
	$(PIP) freeze > etc/requirements.txt
	$(PIP) check

pip_setuptools:
	@echo "pip_setuptools"
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install setuptools wheel
	$(PYTHON) -m pip uninstall artefact_content -y

# -----------------------------------------------------------------------------------------------------
#
#    setup
#
# -----------------------------------------------------------------------------------------------------

setup_development: pip_setuptools
	@echo "setup_development"
	$(PYTHON) setup.py develop

setup_build:
	@echo "build_setup_py"
	$(PIP) install -e .

setup_frontend:
	@echo "setup_frontend"
	$(NPM) -v
	$(NPM) install

# -----------------------------------------------------------------------------------------------------
#
#    venv
#
# -----------------------------------------------------------------------------------------------------

venv:
	@echo "venv_setup"
	$(PYTHON) -m venv venv

venv_clean:
	@echo "venv_clean"
	@echo "deactivate"
	rm -rf venv


# -----------------------------------------------------------------------------------------------------
#
#   download
#
# -----------------------------------------------------------------------------------------------------

download_who:
	mkdir -p $(WHO_SUBDIR)
	wget $(WHO_URL) -O $(WHO_FILE) -o $(WHO_LOG)
	touch $(WHO_SUBDIR)/$(WHO_FILE)
	cp -f $(WHO_SUBDIR)/$(WHO_FILE) $(WHO_SUBDIR)/$(WHO_FILE_BACKUP)
	mv -f $(WHO_FILE) $(WHO_SUBDIR)/$(WHO_FILE)
	mv -f $(WHO_LOG) $(WHO_SUBDIR)/$(WHO_LOG)

download_owid:
	mkdir -p $(OWID_SUBDIR)
	wget $(OWID_URL) -O $(OWID_FILE) -o $(OWID_LOG)
	touch $(OWID_SUBDIR)/$(OWID_FILE)
	cp -f $(OWID_SUBDIR)/$(OWID_FILE) $(OWID_SUBDIR)/$(OWID_FILE_BACKUP)
	mv -f $(OWID_FILE) $(OWID_SUBDIR)/$(OWID_FILE)
	mv -f $(OWID_LOG) $(OWID_SUBDIR)/$(OWID_LOG)

download_rki:
	mkdir -p $(RKI_SUBDIR)
	wget $(RKI_URL) -O $(RKI_FILE) -o $(RKI_LOG)
	touch $(RKI_SUBDIR)/$(RKI_FILE)
	cp -f $(RKI_SUBDIR)/$(RKI_FILE) $(RKI_SUBDIR)/$(RKI_FILE_BACKUP)
	mv -f $(RKI_FILE) $(RKI_SUBDIR)/$(RKI_FILE)
	mv -f $(RKI_LOG) $(RKI_SUBDIR)/$(RKI_LOG)

download_rki_vaccination:
	mkdir -p $(RKI_VACCINATION_SUBDIR)
	wget $(RKI_VACCINATION_URL) -O $(RKI_VACCINATION_FILE) -o $(RKI_VACCINATION_LOG)
	touch $(RKI_VACCINATION_SUBDIR)/$(RKI_VACCINATION_FILE)
	cp -f $(RKI_VACCINATION_SUBDIR)/$(RKI_VACCINATION_FILE) $(RKI_VACCINATION_SUBDIR)/$(RKI_VACCINATION_FILE_BACKUP)
	mv -f $(RKI_VACCINATION_FILE) $(RKI_VACCINATION_SUBDIR)/$(RKI_VACCINATION_FILE)
	mv -f $(RKI_VACCINATION_LOG) $(RKI_VACCINATION_SUBDIR)/$(RKI_VACCINATION_LOG)

download_ecdc:
	mkdir -p $(ECDC_SUBDIR)
	wget $(ECDC_URL) -O $(ECDC_FILE) -o $(ECDC_LOG)
	touch $(ECDC_SUBDIR)/$(ECDC_FILE)
	cp -f $(ECDC_SUBDIR)/$(ECDC_FILE) $(ECDC_SUBDIR)/$(ECDC_FILE_BACKUP)
	mv -f $(ECDC_FILE) $(ECDC_SUBDIR)/$(ECDC_FILE)
	mv -f $(ECDC_LOG) $(ECDC_SUBDIR)/$(ECDC_LOG)

download_divi:
	mkdir -p $(DIVI_SUBDIR)
	wget $(DIVI_URL) -O $(DIVI_FILE) -o $(DIVI_LOG)
	touch $(DIVI_SUBDIR)/$(DIVI_FILE)
	cp -f $(DIVI_SUBDIR)/$(DIVI_FILE) $(DIVI_SUBDIR)/$(DIVI_FILE_BACKUP)
	mv -f $(DIVI_FILE) $(DIVI_SUBDIR)/$(DIVI_FILE)
	mv -f $(DIVI_LOG) $(DIVI_SUBDIR)/$(DIVI_LOG)


# -----------------------------------------------------------------------------------------------------
#
#   stay human
#
# -----------------------------------------------------------------------------------------------------

love:
	@echo "not war!"


# -----------------------------------------------------------------------------------------------------
#
#   main targets
#
# -----------------------------------------------------------------------------------------------------

start: pip_setuptools pip_install setup_frontend

pip_rebuild: pip_compile pip_install pip_check setup_frontend

setup: clean setup_development setup_build

download: download_who download_owid download_rki download_rki_vaccination download_divi download_ecdc
