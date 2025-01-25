#!/bin/bash

python3 manage.py migrate

echo "Collect static files"
python3 manage.py collectstatic --noinput

echo "Create django superuser"
echo "Create user"

python3 manage.py ensure_adminuser --no-input

echo "Starting server backend"
exec "$@"
