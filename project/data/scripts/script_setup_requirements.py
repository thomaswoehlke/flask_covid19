#!/usr/bin/env python
import logging
import os
import subprocess

scripts_dir = "flask_covid19" + os.sep + "app_build" + os.sep + "scripts" + os.sep
pip_requirements_dir = "flask_covid19" + os.sep + "app_build" + os.sep + "requirements"


def run_compile_requirements():
    my_cmd_list = [
        ["pip-compile", "-r", pip_requirements_dir + os.sep + "build.in"],
        ["pip-compile", "-r", pip_requirements_dir + os.sep + "docs.in"],
        ["pip-compile", "-r", pip_requirements_dir + os.sep + "tests.in"],
        ["pip-compile", "-r", pip_requirements_dir + os.sep + "dev.in"],
        ["pip-compile", "-r", pip_requirements_dir + os.sep + "windows.in"],
        ["pip", "install", "-r", pip_requirements_dir + os.sep + "build.txt"],
        ["pip", "install", "-r", pip_requirements_dir + os.sep + "docs.txt"],
        ["pip", "install", "-r", pip_requirements_dir + os.sep + "tests.txt"],
        ["pip", "install", "-r", pip_requirements_dir + os.sep + "dev.txt"],
        # ['pip', 'install', '-r', pip_requirements_dir + os.sep + 'windows.txt'],
    ]
    for my_cmd in my_cmd_list:
        return_code = subprocess.call(my_cmd, shell=True)
        if return_code == 0:
            logging.info("return_code: " + str(return_code))
        else:
            logging.error("return_code: " + str(return_code))
    return None


run_compile_requirements()
