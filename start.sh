#!/bin/bash
pip install -r requirements.txt  # Install dependencies
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
