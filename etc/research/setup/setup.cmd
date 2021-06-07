deactivate
rm -rf venv
py -3 -m venv venv
venv\Scripts\activate
pip install -r etc\requirements.txt
