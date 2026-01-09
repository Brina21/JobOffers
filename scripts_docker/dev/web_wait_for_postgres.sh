#!/bin/bash

# wait for Postgres to start
postgres_ready() {
python << END
import sys
import psycopg2
import os

# leer variables de entorno para desarrollo
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'joboffers')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'admin')

try:
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host="db"
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

# Start app
>&2 echo "Postgres is up - executing command"
sh /scripts_docker/dev/run_web.sh
