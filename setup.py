"""
flask_covid19
-------------
Various utility functions and custom data types for SQLAlchemy.
"""
import logging
import os
import re
import subprocess
import sys

from setuptools import find_packages
from setuptools import setup

HERE = os.path.dirname(os.path.abspath(__file__))


def get_version():
    filename = os.path.join(HERE, "project", "__init__.py")
    with open(filename) as f:
        contents = f.read()
    pattern = r"^__version__ = '(.*?)'$"
    return re.search(pattern, contents, re.MULTILINE).group(1)


scripts_dir = "project" + os.sep + "app_bootstrap" + os.sep + "scripts" + os.sep

pip_requirements_in_dir = (
    "project" + os.sep + "app_bootstrap" + os.sep + "requirements_in"
)

pip_requirements_linux_dir = (
    "project" + os.sep + "app_bootstrap" + os.sep + "requirements_linux"
)

pip_requirements_windows_dir = (
    "project" + os.sep + "app_bootstrap" + os.sep + "requirements_windows"
)


readme = open("docs" + os.sep + "README.md").read()
history = open("docs" + os.sep + "BACKLOG.md").read()

keywords_list = [
    "virus",
    "pandemic",
    "covid19",
    "corona",
    "SARS-CoV-2",
    "WHO",
    "RKI",
    "ECDC",
    "OWID",
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
    "Sphinx",
    "myst-parser",
    "babel>=2.9.1",
    "sphinx-issues",
    "sphinxcontrib-log-cabinet",
    "sphinxcontrib-plantuml",
    "sphinxcontrib-bibtex",
    "sphinxcontrib-images",
    "sphinxcontrib-gravizo",
    "sphinxcontrib-needs",
    "sphinxcontrib-markdown",
    "sphinxcontrib-srclinks",
    "sphinx-tabs",
]

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)

pytest_runner = ["pytest-runner"] if needs_pytest else []

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
    u = os.uname()
    if u.sysname == "Linux":
        pip_requirements_dir = pip_requirements_linux_dir
        my_cmd_list = [
            ["pip-compile", "-r", pip_requirements_in_dir + os.sep + "build.in"],
            ["pip-compile", "-r", pip_requirements_in_dir + os.sep + "docs.in"],
            ["pip-compile", "-r", pip_requirements_in_dir + os.sep + "tests.in"],
            ["pip-compile", "-r", pip_requirements_in_dir + os.sep + "dev.in"],
            ["pip-compile", "-r", pip_requirements_in_dir + os.sep + "linux.in"],
            ["pip", "install", "-r", pip_requirements_dir + os.sep + "build.in"],
            ["pip", "install", "-r", pip_requirements_dir + os.sep + "docs.in"],
            ["pip", "install", "-r", pip_requirements_dir + os.sep + "tests.in"],
            ["pip", "install", "-r", pip_requirements_dir + os.sep + "dev.in"],
            ["pip", "install", "-r", pip_requirements_dir + os.sep + "linux.in"],
        ]
    else:
        pip_requirements_dir = pip_requirements_windows_dir
        my_cmd_list = [
            ["pip-compile", "-r", pip_requirements_in_dir + os.sep + "build.in"],
            ["pip-compile", "-r", pip_requirements_in_dir + os.sep + "docs.in"],
            ["pip-compile", "-r", pip_requirements_in_dir + os.sep + "tests.in"],
            ["pip-compile", "-r", pip_requirements_in_dir + os.sep + "dev.in"],
            ["pip-compile", "-r", pip_requirements_in_dir + os.sep + "windows.in"],
            ["pip", "install", "-r", pip_requirements_dir + os.sep + "build.in"],
            ["pip", "install", "-r", pip_requirements_dir + os.sep + "docs.in"],
            ["pip", "install", "-r", pip_requirements_dir + os.sep + "tests.in"],
            ["pip", "install", "-r", pip_requirements_dir + os.sep + "dev.in"],
            ["pip", "install", "-r", pip_requirements_dir + os.sep + "windows.in"],
        ]
    for my_cmd in my_cmd_list:
        return_code = subprocess.call(my_cmd, shell=True)
        if return_code == 0:
            logging.info("return_code: " + str(return_code))
        else:
            logging.error("return_code: " + str(return_code))
    return None


def run_npm_install():
    my_cmd_list = [
        ["npm", "-y"],
        ["npm", "install"],
    ]
    for my_cmd in my_cmd_list:
        return_code = subprocess.call(my_cmd, shell=True)
        if return_code == 0:
            logging.info("return_code: " + str(return_code))
        else:
            logging.error("return_code: " + str(return_code))
    return None


def get_python_requirements_from_txt():
    my_cmd = ["bash", "scripts" + os.sep + "script_get_python_requirements_from_txt.sh"]
    return_code = subprocess.call(my_cmd, shell=True)
    if return_code == 0:
        logging.info("return_code: " + str(return_code))
    else:
        logging.error("return_code: " + str(return_code))
    return None


setup(
    name="flask_covid19",
    description="Covid19 Data Aggregation "
    + "- also a Project to learn Python Flask, SQLAlchemy, Celery et al.",
    version="0.0.78",
    url="https://github.com/thomaswoehlke/covid19python.git",
    author="Thomas Woehlke",
    author_email="thomas.woehlke@gmail.com",
    license="GNU General Public License v3 (GPLv3)",
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
