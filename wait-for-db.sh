#!/bin/bash
set -e

# Utilisez les variables d'environnement ou des valeurs par défaut
DB_HOST=${MYSQL_HOST:-"localhost"}
DB_PORT=${MYSQL_PORT:-3306}

echo "⌛ Attente de la disponibilité de la base de données sur $DB_HOST:$DB_PORT ..."
while ! nc -z $DB_HOST $DB_PORT; do
    sleep 1
done
echo "✅ La base de données est accessible."
# 9. Run database migrations
echo "Running database migrations..."
alembic upgrade head
# Exécute la commande passée en argument
exec "$@"
