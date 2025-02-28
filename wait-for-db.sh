#!/bin/bash

echo "⏳ Waiting for MySQL at $MYSQL_HOST:$MYSQL_PORT..."

until python3 -c "import pymysql; pymysql.connect(host='$MYSQL_HOST', user='$MYSQL_USER', password='$MYSQL_PASSWORD', database='$MYSQL_DB'); print('✅ MySQL is ready!')" &> /dev/null; do
  echo "🔄 Waiting for database..."
  sleep 3
done

echo "✅ Database is ready! Starting application..."
exec "$@"

