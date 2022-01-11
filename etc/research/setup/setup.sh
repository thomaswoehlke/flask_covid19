#!/app_web_user/bin/env bash

deactivate
rm -rf venv
python3 -m venv venv
. venv/bin/activate
pip install -r etc/requirements.txt
