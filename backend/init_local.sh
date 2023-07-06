#!/bin/sh
python manage.py makemigrations;
python manage.py migrate;
python manage.py createsuperuser --username antares --email antares@food.fk;
python manage.py import_csv;
