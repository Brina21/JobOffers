#!/bin/sh

# wait for Postgres to start
postgres_ready() {
python << END
import sys
import psycopg2

# leer secretos en producción
POSTGRES_DB = "joboffers"
POSTGRES_USER = "admin"
POSTGRES_PASSWORD = open('/run/secrets/POSTGRES_PASSWORD', 'r').read().strip()

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

cd /code

# ejecutar makemigrations si la variable está activada (NO en producción)
if [ "$MAKEMIGRATIONS" = "yes" ]; then
    >&2 echo "Postgres is up - makemigrations"
    python manage.py makemigrations --noinput
fi

# ejecutar migrate si la variable está activada
if [ "$MIGRATE" = "yes" ]; then
    >&2 echo "Postgres is up - migrate"
    python manage.py migrate --noinput
fi

# recolectar archivos estáticos si la variable está activada
if [ "$STATIC" = "yes" ]; then
    >&2 echo "Postgres is up - collecting static"
    python manage.py collectstatic --noinput
fi
