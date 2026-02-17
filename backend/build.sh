#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# One-time setup tasks
python import_jobs_from_csv.py
python import_carriers.py
python import_local_dump.py
python create_admin.py
