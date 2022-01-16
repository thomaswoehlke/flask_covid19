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
UNAME := uname

DB_DIR := project/db
DOCS_DIR := docs
DATA_DIR := data
PIP_REQUIREMENTS_IN_DIR := project/data/requirements_in
PIP_REQUIREMENTS_WINDOWS_DIR := project/data/requirements_windows
PIP_REQUIREMENTS_LINUX_DIR := project/data/requirements_linux

.PHONY: all

all: start

# -------------------------------------------------------------------------------------
#
#    clean
#
# -------------------------------------------------------------------------------------

clean_linux:
	@echo "------------------"
	@echo "making clean_linux"
	@echo "------------------"
	rm -rf .eggs
	rm -rf project.egg-info
	rm -rf flask_covid19.egg-info
	rm -rf build
	rm -rf dist
	rm -rf .checkmate
	rm -rf node_modules
	rm -rf broker
	rm -rf .tox
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	@echo "------------------"
	@echo "making clean_linux DONE"
	@echo "------------------"

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
	@echo "------------------"
	@echo "making pip_compile_windows"
	@echo "------------------"
	python -m pip install --upgrade pip
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_WINDOWS_DIR)/build.txt $(PIP_REQUIREMENTS_IN_DIR)/build.in
	@echo "------------------"
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_WINDOWS_DIR)/docs.txt $(PIP_REQUIREMENTS_IN_DIR)/docs.in
	@echo "------------------"
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_WINDOWS_DIR)/tests.txt $(PIP_REQUIREMENTS_IN_DIR)/tests.in
	@echo "------------------"
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_WINDOWS_DIR)/typing.txt $(PIP_REQUIREMENTS_IN_DIR)/typing.in
	@echo "------------------"
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_WINDOWS_DIR)/dev.txt $(PIP_REQUIREMENTS_IN_DIR)/dev.in
	@echo "------------------"
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_WINDOWS_DIR)/windows.txt $(PIP_REQUIREMENTS_IN_DIR)/windows.in
	@echo "------------------"
	@echo "making pip_compile_windows DONE"
	@echo "------------------"

pip_compile_linux:
	@echo "------------------"
	@echo "making pip_compile_linux"
	@echo "------------------"
	python -m pip install --upgrade pip
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_LINUX_DIR)/build.txt $(PIP_REQUIREMENTS_IN_DIR)/build.in
	@echo "------------------"
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_LINUX_DIR)/docs.txt $(PIP_REQUIREMENTS_IN_DIR)/docs.in
	@echo "------------------"
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_LINUX_DIR)/tests.txt $(PIP_REQUIREMENTS_IN_DIR)/tests.in
	@echo "------------------"
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_LINUX_DIR)/typing.txt $(PIP_REQUIREMENTS_IN_DIR)/typing.in
	@echo "------------------"
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_LINUX_DIR)/dev.txt $(PIP_REQUIREMENTS_IN_DIR)/dev.in
	@echo "------------------"
	$(PIP_COMPILE) -r --output-file $(PIP_REQUIREMENTS_LINUX_DIR)/linux.txt $(PIP_REQUIREMENTS_IN_DIR)/linux.in
	@echo "------------------"
	@echo "making pip_compile_linux DONE"
	@echo "------------------"

pip_install_windows_build:
	@echo "------------------"
	@echo "making pip_install"
	@echo "------------------"
	$(PIP) install -r $(PIP_REQUIREMENTS_WINDOWS_DIR)/build.txt
	@echo "------------------"

pip_install_windows: pip_install_windows_build
	@echo "------------------"
	@echo "making pip_install"
	@echo "------------------"
	$(PIP) install -r $(PIP_REQUIREMENTS_WINDOWS_DIR)/docs.txt
	@echo "------------------"
	$(PIP) install -r $(PIP_REQUIREMENTS_WINDOWS_DIR)/tests.txt
	@echo "------------------"
	$(PIP) install -r $(PIP_REQUIREMENTS_WINDOWS_DIR)/typing.txt
	@echo "------------------"
	$(PIP) install -r $(PIP_REQUIREMENTS_WINDOWS_DIR)/dev.txt
	@echo "------------------"
	$(PIP) install -r $(PIP_REQUIREMENTS_WINDOWS_DIR)/windows.txt
	@echo "------------------"
	$(PIP) freeze > etc/requirements_windows.txt
	@echo "------------------"
	$(PIP) check
	@echo "------------------"
	@echo "making pip_install DONE"
	@echo "------------------"

pip_install_linux_build:
	@echo "------------------"
	@echo "making pip_install_linux_build"
	@echo "------------------"
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r $(PIP_REQUIREMENTS_LINUX_DIR)/build.txt
	$(PIP) freeze > etc/requirements_linux.txt
	$(PIP) check
	@echo "------------------"
	@echo "making pip_install_linux_build DONE"
	@echo "------------------"

pip_install_linux: pip_install_linux_build
	@echo "------------------"
	@echo "making pip_install_linux"
	@echo "------------------"
	# $(PIP) install -r $(PIP_REQUIREMENTS_LINUX_DIR)/build.txt
	@echo "------------------"
	@echo "making pip_install_linux docs.txt"
	@echo "------------------"
	$(PIP) install -r $(PIP_REQUIREMENTS_LINUX_DIR)/docs.txt
	@echo "------------------"
	@echo "making pip_install_linux tests.txt"
	@echo "------------------"
	$(PIP) install -r $(PIP_REQUIREMENTS_LINUX_DIR)/tests.txt
	@echo "------------------"
	@echo "making pip_install_linux typing.txt"
	$(PIP) install -r $(PIP_REQUIREMENTS_LINUX_DIR)/typing.txt
	@echo "------------------"
	@echo "making pip_install_linux dev.txt"
	$(PIP) install -r $(PIP_REQUIREMENTS_LINUX_DIR)/dev.txt
	@echo "------------------"
	@echo "making pip_install_linux linux.txt"
	$(PIP) install -r $(PIP_REQUIREMENTS_LINUX_DIR)/linux.txt
	$(PIP) freeze > etc/requirements_linux.txt
	$(PIP) check
	@echo "------------------"
	@echo "making pip_install_linux DONE"
	@echo "------------------"

pip_uninstall_linux:
	@echo "------------------"
	@echo "making pip_uninstall_linux"
	@echo "------------------"
	$(PIP) freeze > etc/requirements_linux.txt
	@echo "------------------"
	$(PIP) uninstall -r etc/requirements_linux.txt -y
	@echo "------------------"
	$(PIP) check
	@echo "------------------"
	@echo "making pip_uninstall_linux DONE"
	@echo "------------------"

# -------------------------------------------------------------------------------------
#
#    setup.py
#
# -------------------------------------------------------------------------------------

setup_setuptools:
	@echo "------------------"
	@echo "making setup_setuptools"
	@echo "------------------"
	$(PYTHON) -m pip install --upgrade pip
	# $(PYTHON) -m pip install --upgrade setuptools
	# $(PYTHON) -m pip install --upgrade wheel
	# $(PYTHON) -m pip install setuptools wheel
	# $(PYTHON) -m pip uninstall $(APP_MYSELF) -y
	@echo "------------------"
	@echo "making setup_setuptools DONE"
	@echo "------------------"

setup_development: pip_setuptools
	@echo "making setup_development"
	$(PYTHON) setup.py develop
	@echo "making setup_development DONE"

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
	@echo "------------------"
	@echo "making venv_setup"
	@echo "------------------"
	$(PYTHON) -m venv venv
	@echo "------------------"
	@echo "making venv_setup DONE"
	@echo "------------------"

venv_clean:
	@echo "------------------"
	@echo "making venv_clean"
	@echo "------------------"
	@echo "deactivate"
	@echo "------------------"
	rm -rf venv
	@echo "------------------"
	@echo "making venv_clean DONE"
	@echo "------------------"


# -------------------------------------------------------------------------------------
#
#    Renv
#
# -------------------------------------------------------------------------------------

renv:
	@echo "------------------"
	@echo "making venv_setup"
	@echo "------------------"
	@echo "TBD"
	@echo "------------------"

renv_clean:
	@echo "------------------"
	@echo "making venv_clean"
	@echo "------------------"
	@echo "deactivate"
	@echo "------------------"
	rm -rf renv
	@echo "------------------"

# -------------------------------------------------------------------------------------
#
#   stay human
#
# -------------------------------------------------------------------------------------

love:
	@echo "------------------"
	@echo "not war!"
	@echo "------------------"


# -------------------------------------------------------------------------------------
#
#   SCM targets
#
# -------------------------------------------------------------------------------------

git:
	@echo "------------------"
	@echo "making git"
	@echo "------------------"
	$(GIT) fetch
	$(GIT) status
	$(GIT) add -u
	$(GIT) commit -m "work"
	$(GIT) status
	@$(GIT) push
	$(GIT) fetch
	$(GIT) status
	@echo "------------------"
	@echo "making git DONE"
	@echo "------------------"

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
	@echo "------------------"
	@echo "making setup_frontend"
	@echo "------------------"
	$(NPM) -v
	$(NPM) install
	@echo "------------------"
	@echo "making setup_frontend DONE"
	@echo "------------------"

setup_npm:
	@echo "------------------"
	@echo "making setup_npm"
	@echo "------------------"
	sudo npm install -g npm
	@echo "------------------"
	@echo "making setup_npm DONE"
	@echo "------------------"


distclean: venv_clean renv_clean

update_windows: clean_windows pip_compile_windows pip_install_windows pip_check setup_frontend

update_linux: clean_linux pip_compile_linux pip_install_linux pip_check setup_frontend

start_windows: pip_install_windows_build update_windows

start_linux: pip_install_linux_build update_linux

update:
ifeq ($(UNAME),"Linux")
	make update_linux
else
	make update_windows
endif

start:
ifeq ($(UNAME),"Linux")
	make start_linux
else
	make start_windows
endif

