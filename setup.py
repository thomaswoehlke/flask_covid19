import logging
import os
import subprocess
import sys

from setuptools import find_packages
from setuptools import setup

version = "0.0.73"

scripts_dir = "flask_covid19" + os.sep + "app_build" + os.sep + "scripts" + os.sep
pip_requirements_dir = "flask_covid19" + os.sep + "app_build" + os.sep + "requirements"

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []

readme = open("README.md").read()
history = open("docs" + os.sep + "BACKLOG.md").read()

keywords_list = [
    "virus",
    "pandemic",
    "covid19",
    "corona",
    "who",
    "rki",
    "ecdc",
    "deaths",
    "cases",
    "vaccination",
    "data",
    "statistic",
    "python",
    "flask",
    "celery",
    "sqlalchemy",
    "mysql",
]

requires_build = [
    "wheel",
    "pip-tools",
    "pipenv",
    "virtualenv",
    "pytoolbox",
    "python-dotenv",
    "tox",
    "toml",
    "Flask",
    "urllib3>=1.26.5",
    "pillow>=8.3.2",
]

requires_test = [
    "pytest",
    "pytest-runner",
    "pytest-flask",
    "pytest-flask-sqlalchemy",
]

requires_docs = [
    "Pallets-Sphinx-Themes",
    # "sphinx_bootstrap_theme",
    "sphinx",
    "myst-parser",
    # "sphinx-issues",
    # "sphinxcontrib-log-cabinet",
    # "sphinxcontrib-plantuml",
    # "sphinxcontrib-bibtex",
    # "sphinxcontrib-images",
    # "sphinxcontrib-gravizo",
    # "sphinxcontrib-needs",
    # "sphinxcontrib-markdown",
    # "sphinxcontrib-srclinks",
    # "sphinx-tabs",
]

dotenv_require = ["python-dotenv", "tqdm"]

requires_extras = {
    "docs": requires_docs,
    "tests": requires_test,
    "dotenv": dotenv_require,
    "all": [],
}

requires_dev = [
    "Flask-SQLAlchemy",
    "Flask-Migrate",
    "Flask-Cors",
    "Flask-BS4>=5.0.0.1",
    "Flask-Admin",
    "Flask-Login",
    "flask-login-dictabase-blueprint",
    "SQLAlchemy",
    "sqlalchemy-mixins",
    "mysql-connector-python",
    "mysqldb-wrapper",
    "mariadb",
    "wget",
    "email_validator",
    "celery[redis,sqlalchemy,auth,msgpack,eventlet]>=5.1",
    "dataframetodb",
    "pangres",
    "scipy",
    "matplotlib",
    "statsmodels",
    "pandas",
] + pytest_runner


for reqs in requires_extras.values():
    requires_extras["all"].extend(reqs)

keywords = ""
for kw in keywords_list:
    keywords += " " + kw

packages = find_packages()


def run_compile_requirements():
    my_cmd_list = [
        ["pip-compile", "-r", pip_requirements_dir + os.sep + "build.in"],
        ["pip-compile", "-r", pip_requirements_dir + os.sep + "docs.in"],
        ["pip-compile", "-r", pip_requirements_dir + os.sep + "tests.in"],
        ["pip-compile", "-r", pip_requirements_dir + os.sep + "dev.in"],
        ["pip", "install", "-r", pip_requirements_dir + os.sep + "build.in"],
        ["pip", "install", "-r", pip_requirements_dir + os.sep + "docs.in"],
        ["pip", "install", "-r", pip_requirements_dir + os.sep + "tests.in"],
        ["pip", "install", "-r", pip_requirements_dir + os.sep + "dev.in"],
    ]
    for my_cmd in my_cmd_list:
        returncode = subprocess.call(my_cmd, shell=True)
        if returncode == 0:
            logging.info("retcode: " + str(returncode))
        else:
            logging.error("retcode: " + str(returncode))
    return None


def run_npm_install():
    my_cmd = ["npm", "install"]
    returncode = subprocess.call(my_cmd, shell=True)
    if returncode == 0:
        logging.info("retcode: " + str(returncode))
    else:
        logging.error("retcode: " + str(returncode))
    return None


def get_python_requirements_from_txt():
    my_cmd = ["bash", "scripts" + os.sep + "script_get_python_requirements_from_txt.sh"]
    returncode = subprocess.call(my_cmd, shell=True)
    if returncode == 0:
        logging.info("retcode: " + str(returncode))
    else:
        logging.error("retcode: " + str(returncode))
    return None


setup(
    name="flask-covid19",
    version=version,
    url="https://github.com/thomaswoehlke/covid19python.git",
    license="GNU General Public License v3 (GPLv3)",
    author="Thomas Woehlke",
    author_email="thomas.woehlke@gmail.com",
    description="Covid19 Data Aggregation - also a Project to learn Python Flask, SQLAlchemy, Celery et al.",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 3 - Alpha",
        "Natural Language :: German",
        "Natural Language :: English",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database :: Frontends",
        "Framework :: Flask",
    ],
    long_description=readme + history,
    long_description_content_type="text/markdown",
    keywords=keywords,
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    entry_points={},
    extras_require=requires_extras,
    install_requires=requires_dev,
    setup_requires=requires_build,
    tests_require=requires_test,
    scripts=[
        scripts_dir + "script_setup_requirements.py",
        scripts_dir + "script_npm_install.py",
    ],
    python_requires=">= 3.9",
)
