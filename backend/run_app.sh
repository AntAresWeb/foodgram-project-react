#!/bin/sh
python manage.py makemigrations;
python manage.py migrate;
python manage.py collectstatic --noinput;
gunicorn -b 0.0.0.0:8008 foodgram.wsgi;
#python manage.py runserver 0.0.0.0:8008