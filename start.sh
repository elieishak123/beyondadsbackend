#!/bin/bash
pip install --upgrade pip
pip install --force-reinstall -r requirements.txt
gunicorn backend.backend.wsgi:application --bind 0.0.0.0:$PORT
