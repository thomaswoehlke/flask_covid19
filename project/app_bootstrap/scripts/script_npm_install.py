#!/app_web_user/bin/env python
import logging
import subprocess


def run_npm_install():
    my_cmd = ["npm", "install"]
    return_code = subprocess.call(my_cmd, shell=True)
    if return_code == 0:
        logging.info("return_code: " + str(return_code))
    else:
        logging.error("return_code: " + str(return_code))
    return None


run_npm_install()
