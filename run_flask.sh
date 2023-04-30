#!/bin/bash 

python -m venv venv
source venv/bin/activate
pip install flask
set FLASK_APP=app.py
DATABASE_URL=postgresql://postgres@localhost:5432/group_test5
flask run --debug
