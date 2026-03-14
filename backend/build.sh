#!/usr/bin/env bash

pip install -r requirement.txt
python manage.py collectstatic --noinput
python manage.py migrate