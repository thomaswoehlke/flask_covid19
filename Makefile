DATA_DIR := data
DB_DIR := db

.PHONY: all

all: clean setup


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
#    setup
#
# -----------------------------------------------------------------------------------------------------

setup: clean setup_development_setuptools setup_pip_install setup_pip_compile setup_pip_install setup_pip_check setup_development setup_frontend

setup_pip_check:
	@echo "setup_pip_check"
	python -m pip check

setup_pip_compile:
	@echo "setup_pip_compile"
	pip-compile -r requirements/build.in
	pip-compile -r requirements/docs.in
	pip-compile -r requirements/tests.in
	pip-compile -r requirements/dev.in

setup_pip_install:
	@echo "pip_install"
	pip install -r requirements/build.txt
	pip install -r requirements/docs.txt
	pip install -r requirements/tests.txt
	pip install -r requirements/dev.txt
	# . scripts/script_get_python_requirements_from_txt.sh
	pip freeze > etc/requirements.txt
	pip check

setup_development_setuptools:
	@echo "setup_development_pip"
	python -m pip install --upgrade pip
	python -m pip install setuptools wheel
	python -m pip uninstall artefact_content -y

setup_development: setup_development_setuptools
	@echo "setup_development"
	python setup.py develop

setup_frontend:
	@echo "setup_frontend"
	npm -v
	npm install


# -----------------------------------------------------------------------------------------------------
#
#    build
#
# -----------------------------------------------------------------------------------------------------

build: build_setup_py

build_setup_py:
	@echo "build_setup_py"
	pip install -e .


# -----------------------------------------------------------------------------------------------------
#
#    venv
#
# -----------------------------------------------------------------------------------------------------

venv_setup:
	@echo "venv_setup"
	python3 -m venv venv

venv_clean:
	@echo "venv_clean"
	@echo "deactivate"
	rm -rf venv

# -----------------------------------------------------------------------------------------------------
#
#   data
#
# -----------------------------------------------------------------------------------------------------

download:
	$(MAKE) -C $(DATA_DIR) download

db:	db_dumb

db_dumb:
	$(MAKE) -C $(DB_DIR) db

# -----------------------------------------------------------------------------------------------------
#
#   vcs
#
# -----------------------------------------------------------------------------------------------------

vcs_setup:
	git config pull.rebase false
	git submodule init
	git submodule update
	git config --global diff.submodule log
	git submodule update --remote --merge

vcs_commit:
	git add .
	git commit -m "git_commit_and_push via make"

vcs_update:
	git submodule update
	git pull $(REMOTE) $(REMOTE_BRANCH)

vcs_store_to_remote:
	git push $(REMOTE) $(REMOTE_BRANCH)

vcs_push: vcs_setup vcs_commit vcs_store_to_remote vcs_load_from_remote

vcs_pull: vcs_setup vcs_checkout

vcs: vcs_push

# -----------------------------------------------------------------------------------------------------
#
#   stay human
#
# -----------------------------------------------------------------------------------------------------

love:
	@echo "not war!"


start: setup_pip_install setup_frontend




