#!/usr/bin/bash

echo "Cleaning up database file..."
rm -v /home/k26ra/code/mad2-project-rahul/backend/instance/demo.db

echo "Cleaning up Redis dump..."
rm -v /home/k26ra/code/mad2-project-rahul/backend/dump.rdb

echo "Cleaning up Celery schedule file..."
rm -v /home/k26ra/code/mad2-project-rahul/backend/celerybeat-schedule

echo "Cleaning up Python cache directories..."
find /home/k26ra/code/mad2-project-rahul/backend -type d -name "__pycache__" -exec rm -rv {} +

echo "Starting the application..."
nodemon --exec py -m app