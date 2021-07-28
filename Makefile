TZ := 'Europe/Berlin'
HEUTE := backup
HEUTE_todo := "date '+%Y_%m_%d'"

APP_MYSELF := flask_covid19
DATA_DIR := flask_covid19/data
DB_DIR := flask_covid19/db
PYTHON := python
PIP_COMPILE := pip-compile
PIP := pip
NPM := npm
PIP_REQUIREMENTS_DIR := flask_covid19/app_build/requirements


WHO_URL := https://covid19.who.int/WHO-COVID-19-global-data.csv
WHO_FILE_BACKUP := WHO-$(HEUTE).csv
WHO_FILE := WHO.csv
WHO_LOG := WHO.csv.log
WHO_SUBDIR := $(DATA_DIR)/who

OWID_URL := https://covid.ourworldindata.org/data/owid-covid-data.csv
OWID_FILE_BACKUP := OWID-$(HEUTE).csv
OWID_FILE := OWID.csv
OWID_LOG := OWID.csv.log
OWID_SUBDIR := $(DATA_DIR)/owid

RKI_URL := https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data
RKI_FILE_BACKUP := RKI-$(HEUTE).csv
RKI_FILE := RKI.csv
RKI_LOG := RKI.csv.log
RKI_SUBDIR := $(DATA_DIR)/rki

RKI_VACCINATION_URL := https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv
RKI_VACCINATION_FILE_BACKUP := Vaccination-$(HEUTE).tsv
RKI_VACCINATION_FILE := Vaccination.tsv
RKI_VACCINATION_LOG := Vaccination.tsv.log
RKI_VACCINATION_SUBDIR := $(DATA_DIR)/vaccination

DIVI_URL := https://www.intensivregister.de/api/public/intensivregister
DIVI_FILE_BACKUP := DIVI-$(HEUTE).json
DIVI_FILE := DIVI.json
DIVI_LOG := DIVI.json.log
DIVI_SUBDIR := $(DATA_DIR)/divi

ECDC_URL := https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/
ECDC_FILE_BACKUP := ECDC-$(HEUTE).csv
ECDC_FILE := ECDC.csv
ECDC_LOG := ECDC.csv.log
ECDC_SUBDIR := $(DATA_DIR)/ecdc

.PHONY: all

all: start


# -----------------------------------------------------------------------------------------------------
#
#    clean
#
# -----------------------------------------------------------------------------------------------------

clean_linux:
	@echo "clean_linux"
	rm -rf .eggs
	rm -rf artefact_content.egg-info
	rm -rf build
	rm -rf dist
	rm -rf .checkmate
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean_windows:
	@echo "clean_windows"
	@echo "TBD"

clean_mac: clean_linux
	@echo "clean_mac"
	@echo "TBD"

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

pip_compile_windows: pip_compile
	@echo "pip_compile_windows"
	$(PIP_COMPILE) -r $(PIP_REQUIREMENTS_DIR)/windows.in

pip_install_windows: pip_install
	@echo "pip_install_windows"
	$(PIP) install -r $(PIP_REQUIREMENTS_DIR)/windows.txt
	$(PIP) freeze > etc/requirements.txt
	$(PIP) check

pip_compile_linux: pip_compile
	@echo "pip_compile_linux"
	$(PIP_COMPILE) -r $(PIP_REQUIREMENTS_DIR)/linux.in

pip_install_linux: pip_install
	@echo "pip_install_windows"
	$(PIP) install -r $(PIP_REQUIREMENTS_DIR)/linux.txt
	$(PIP) freeze > etc/requirements.txt
	$(PIP) check

pip_compile_mac: pip_compile
	@echo "pip_compile_mac"
	$(PIP_COMPILE) -r $(PIP_REQUIREMENTS_DIR)/mac.in

pip_install_mac: pip_install
	@echo "pip_install_windows"
	$(PIP) install -r $(PIP_REQUIREMENTS_DIR)/mac.txt
	$(PIP) freeze > etc/requirements.txt
	$(PIP) check

pip_setuptools:
	@echo "pip_setuptools"
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install setuptools wheel
	$(PYTHON) -m pip uninstall $(APP_MYSELF) -y

pip_uninstall:
	@echo "pip_uninstall"
	$(PIP) freeze > etc/requirements.txt
	$(PIP) uninstall -r etc/requirements.txt -y
	$(PIP) check

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
#    venv + renv
#
# -----------------------------------------------------------------------------------------------------

venv:
	@echo "venv_setup"
	$(PYTHON) -m venv venv

venv_clean:
	@echo "venv_clean"
	@echo "deactivate"
	rm -rf venv

renv:
	@echo "venv_setup"
	@echo "TBD"

renv_clean:
	@echo "venv_clean"
	@echo "deactivate"
	rm -rf renv


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
	mv -f $(OWID_FILE) $(OWID_SUBDIR)/$(OWID_FILE)
	mv -f $(OWID_LOG) $(OWID_SUBDIR)/$(OWID_LOG)
	cp -f $(OWID_SUBDIR)/$(OWID_FILE) $(OWID_SUBDIR)/$(OWID_FILE_BACKUP)

download_rki:
	mkdir -p $(RKI_SUBDIR)
	wget $(RKI_URL) -O $(RKI_FILE) -o $(RKI_LOG)
	touch $(RKI_SUBDIR)/$(RKI_FILE)
	mv -f $(RKI_FILE) $(RKI_SUBDIR)/$(RKI_FILE)
	mv -f $(RKI_LOG) $(RKI_SUBDIR)/$(RKI_LOG)
	cp -f $(RKI_SUBDIR)/$(RKI_FILE) $(RKI_SUBDIR)/$(RKI_FILE_BACKUP)

download_rki_vaccination:
	mkdir -p $(RKI_VACCINATION_SUBDIR)
	wget $(RKI_VACCINATION_URL) -O $(RKI_VACCINATION_FILE) -o $(RKI_VACCINATION_LOG)
	touch $(RKI_VACCINATION_SUBDIR)/$(RKI_VACCINATION_FILE)
	mv -f $(RKI_VACCINATION_FILE) $(RKI_VACCINATION_SUBDIR)/$(RKI_VACCINATION_FILE)
	mv -f $(RKI_VACCINATION_LOG) $(RKI_VACCINATION_SUBDIR)/$(RKI_VACCINATION_LOG)
	cp -f $(RKI_VACCINATION_SUBDIR)/$(RKI_VACCINATION_FILE) $(RKI_VACCINATION_SUBDIR)/$(RKI_VACCINATION_FILE_BACKUP)

download_ecdc:
	mkdir -p $(ECDC_SUBDIR)
	wget $(ECDC_URL) -O $(ECDC_FILE) -o $(ECDC_LOG)
	touch $(ECDC_SUBDIR)/$(ECDC_FILE)
	mv -f $(ECDC_FILE) $(ECDC_SUBDIR)/$(ECDC_FILE)
	mv -f $(ECDC_LOG) $(ECDC_SUBDIR)/$(ECDC_LOG)
	cp -f $(ECDC_SUBDIR)/$(ECDC_FILE) $(ECDC_SUBDIR)/$(ECDC_FILE_BACKUP)

download_divi:
	mkdir -p $(DIVI_SUBDIR)
	wget $(DIVI_URL) -O $(DIVI_FILE) -o $(DIVI_LOG)
	touch $(DIVI_SUBDIR)/$(DIVI_FILE)
	mv -f $(DIVI_FILE) $(DIVI_SUBDIR)/$(DIVI_FILE)
	mv -f $(DIVI_LOG) $(DIVI_SUBDIR)/$(DIVI_LOG)
	cp -f $(DIVI_SUBDIR)/$(DIVI_FILE) $(DIVI_SUBDIR)/$(DIVI_FILE_BACKUP)


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

distclean: venv_clean renv_clean

start: pip_setuptools pip_install setup_frontend

pip: pip_compile pip_install pip_check setup_frontend

windows: clean_windows pip_compile_windows pip_install_windows pip_check setup_frontend

linux: clean_linux pip_compile_linux pip_install_linux pip_check setup_frontend

mac: clean_mac pip_compile_mac pip_install_mac pip_check setup_frontend

setup: clean setup_development setup_build

download: download_who download_owid download_rki download_rki_vaccination download_divi download_ecdc
