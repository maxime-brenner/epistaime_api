#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "En attente de postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL démarré"
fi
exec "$@"