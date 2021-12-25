TZ := 'Europe/Berlin'
HEUTE := backup
HEUTE_todo := "date '+%Y_%m_%d'"

APP_MYSELF := flask_covid19
PYTHON := python
PIP_COMPILE := pip-compile
PIP := pip
NPM := npm
GIT := git
MAKE := make

DB_DIR := project/db
DOCS_DIR := docs
DATA_DIR := data
PIP_REQUIREMENTS_IN_DIR := project/app_bootstrap/requirements_in
PIP_REQUIREMENTS_WINDOWS_DIR := project/app_bootstrap/requirements_windows
PIP_REQUIREMENTS_LINUX_DIR := project/app_bootstrap/requirements_linux

.PHONY: all

all: start

# -------------------------------------------------------------------------------------
#
#    clean
#
# -------------------------------------------------------------------------------------

clean_linux:
	@echo "clean_linux"
	rm -rf .eggs
	rm -rf project.egg-info
	rm -rf build
	rm -rf dist
	rm -rf .checkmate
	rm -rf node_modules
	rm -rf .tox
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean_windows:
	@echo "clean_windows"
	@echo "TBD"

clean:	clean_linux

# -------------------------------------------------------------------------------------
#
#    pip
#
# -------------------------------------------------------------------------------------

pip_check:
	@echo "pip_check"
	$(PYTHON) -m pip check

pip_compile_windows:
	@echo "pip_compile_windows"
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_WINDOWS_DIR)/build.txt $(PIP_REQUIREMENTS_IN_DIR)/build.in
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_WINDOWS_DIR)/docs.txt $(PIP_REQUIREMENTS_IN_DIR)/docs.in
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_WINDOWS_DIR)/tests.txt $(PIP_REQUIREMENTS_IN_DIR)/tests.in
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_WINDOWS_DIR)/typing.txt $(PIP_REQUIREMENTS_IN_DIR)/typing.in
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_WINDOWS_DIR)/dev.txt $(PIP_REQUIREMENTS_IN_DIR)/dev.in
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_WINDOWS_DIR)/windows.txt $(PIP_REQUIREMENTS_IN_DIR)/windows.in

pip_compile_linux:
	@echo "pip_compile_linux"
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_LINUX_DIR)/build.txt $(PIP_REQUIREMENTS_IN_DIR)/build.in
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_LINUX_DIR)/docs.txt $(PIP_REQUIREMENTS_IN_DIR)/docs.in
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_LINUX_DIR)/tests.txt $(PIP_REQUIREMENTS_IN_DIR)/tests.in
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_LINUX_DIR)/typing.txt $(PIP_REQUIREMENTS_IN_DIR)/typing.in
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_LINUX_DIR)/dev.txt $(PIP_REQUIREMENTS_IN_DIR)/dev.in
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_LINUX_DIR)/linux.txt $(PIP_REQUIREMENTS_IN_DIR)/linux.in

pip_install_windows:
	@echo "pip_install"
	$(PIP) install -r $(PIP_REQUIREMENTS_WINDOWS_DIR)/build.txt
	$(PIP) install -r $(PIP_REQUIREMENTS_WINDOWS_DIR)/docs.txt
	$(PIP) install -r $(PIP_REQUIREMENTS_WINDOWS_DIR)/tests.txt
	$(PIP) install -r $(PIP_REQUIREMENTS_WINDOWS_DIR)/typing.txt
	$(PIP) install -r $(PIP_REQUIREMENTS_WINDOWS_DIR)/dev.txt
	$(PIP) install -r $(PIP_REQUIREMENTS_WINDOWS_DIR)/windows.txt
	$(PIP) freeze > etc/requirements_windows.txt
	$(PIP) check

pip_install_linux_build:
	@echo "pip_install_linux_build"
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r $(PIP_REQUIREMENTS_LINUX_DIR)/build.txt
	$(PIP) freeze > etc/requirements_linux.txt
	$(PIP) check

pip_install_linux: pip_install_linux_build
	@echo "pip_install_linux"
	# $(PIP) install -r $(PIP_REQUIREMENTS_LINUX_DIR)/build.txt
	$(PIP) install -r $(PIP_REQUIREMENTS_LINUX_DIR)/docs.txt
	$(PIP) install -r $(PIP_REQUIREMENTS_LINUX_DIR)/tests.txt
	$(PIP) install -r $(PIP_REQUIREMENTS_LINUX_DIR)/typing.txt
	$(PIP) install -r $(PIP_REQUIREMENTS_LINUX_DIR)/dev.txt
	$(PIP) install -r $(PIP_REQUIREMENTS_LINUX_DIR)/linux.txt
	$(PIP) freeze > etc/requirements_linux.txt
	$(PIP) check

pip_uninstall:
	@echo "pip_uninstall"
	$(PIP) freeze > etc/requirements.txt
	$(PIP) uninstall -r etc/requirements.txt -y
	$(PIP) check

# -------------------------------------------------------------------------------------
#
#    setup.py
#
# -------------------------------------------------------------------------------------

pip_setuptools:
	@echo "pip_setuptools"
	$(PYTHON) -m pip install --upgrade pip
	# $(PYTHON) -m pip install --upgrade setuptools
	# $(PYTHON) -m pip install --upgrade wheel
	# $(PYTHON) -m pip install setuptools wheel
	# $(PYTHON) -m pip uninstall $(APP_MYSELF) -y

setup_development: pip_setuptools
	@echo "setup_development"
	$(PYTHON) setup.py develop

flask_covid19_clean:
	@echo "------------------"
	@echo "making flask_covid19"
	@echo "------------------"
	$(PYTHON) -m pip uninstall $(APP_MYSELF) -y
	@echo "------------------"
	@echo "making flask_covid19 DONE"
	@echo "------------------"

flask_covid19:
	@echo "------------------"
	@echo "making flask_covid19"
	@echo "------------------"
	$(PIP) install -e .
	@echo "------------------"
	@echo "making flask_covid19 DONE"
	@echo "------------------"

# -------------------------------------------------------------------------------------
#
#    venv + renv
#
# -------------------------------------------------------------------------------------

venv:
	@echo "venv_setup"
	$(PYTHON) -m venv venv

venv_clean:
	@echo "venv_clean"
	@echo "deactivate"
	rm -rf venv


# -------------------------------------------------------------------------------------
#
#    Renv
#
# -------------------------------------------------------------------------------------

renv:
	@echo "venv_setup"
	@echo "TBD"

renv_clean:
	@echo "venv_clean"
	@echo "deactivate"
	rm -rf renv

# -------------------------------------------------------------------------------------
#
#   stay human
#
# -------------------------------------------------------------------------------------

love:
	@echo "not war!"


# -------------------------------------------------------------------------------------
#
#   SCM targets
#
# -------------------------------------------------------------------------------------

git:
	@echo "--------"
	@echo "making git"
	@echo "--------"
	$(GIT) fetch
	$(GIT) status
	$(GIT) add -u
	$(GIT) commit -m "work"
	$(GIT) status
	@$(GIT) push
	$(GIT) fetch
	$(GIT) status
	@echo "--------"
	@echo "making git DONE"
	@echo "--------"

# -------------------------------------------------------------------------------------
#
#   main targets
#
# -------------------------------------------------------------------------------------

doc:
	@echo "------------------"
	@echo "making doc"
	@echo "------------------"
	$(MAKE) -w -C $(DOCS_DIR) html
	@echo "------------------"
	@echo "making doc DONE"
	@echo "------------------"

test:
	@echo "------------------"
	@echo "making test"
	@echo "------------------"
	pytest -v
	@echo "------------------"
	@echo "making test DONE"
	@echo "------------------"

download:
	@echo "------------------"
	@echo "download"
	@echo "------------------"
	$(MAKE) -w -C $(DATA_DIR) download
	@echo "------------------"
	@echo "download DONE"
	@echo "------------------"

# -------------------------------------------------------------------------------------
#
#   frontend
#
# -------------------------------------------------------------------------------------

setup_frontend:
	@echo "setup_frontend"
	$(NPM) -v
	$(NPM) install

setup_npm:
	@echo "setup_npm"
	sudo npm install -g npm

distclean: venv_clean renv_clean

pip_windows: pip_compile_windows pip_install_windows pip_check setup_frontend

pip_linux: pip_compile_linux pip_install_linux pip_check setup_frontend

windows: clean_windows pip_windows

linux: clean_linux pip_linux

# setup: clean setup_development setup_build

start_windows: pip_setuptools pip_install_windows setup_frontend

start_linux: pip_setuptools pip_install_linux_build linux
