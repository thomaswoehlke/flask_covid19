#!/usr/bin/env python

import os
import subprocess
import logging


def run_compile_requirements():
    my_cmd_list = [
        ['pip-compile', '-r', 'requirements' + os.sep + 'build.in'],
        ['pip-compile', '-r', 'requirements' + os.sep + 'docs.in'],
        ['pip-compile', '-r', 'requirements' + os.sep + 'tests.in'],
        ['pip-compile', '-r', 'requirements' + os.sep + 'dev.in'],
        ['pip', 'install', '-r', 'requirements' + os.sep + 'build.in'],
        ['pip', 'install', '-r', 'requirements' + os.sep + 'docs.in'],
        ['pip', 'install', '-r', 'requirements' + os.sep + 'tests.in'],
        ['pip', 'install', '-r', 'requirements' + os.sep + 'dev.in'],
    ]
    for my_cmd in my_cmd_list:
        return_code = subprocess.call(my_cmd, shell=True)
        if return_code == 0:
            logging.info("return_code: "+str(return_code))
        else:
            logging.error("return_code: " + str(return_code))
    return None


run_compile_requirements()
