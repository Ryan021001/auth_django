#! /bin/bash
set -e
worker=${WORKER:-1}
port=${DJANGO_PORT:-8080}

while ! mysql -h ${DATABASE_HOST:-db} -p ${DATABASE_PORT:-3306} -u ${DATABASE_HOST} -p ${DATABASE_PASSWORD} | grep -q '1'; do
  echo "Cannot connect to database, retrying in 4 seconds..."
  sleep 4
done
echo "Database Ready, Starting..."

python manage.py migrate
python manage.py loaddata scripts/fixtures/*.yaml
python manage.py compilemessages -l en -l ja
python manage.py collectstatic --no-input

if [ "$PRODUCTION" == "TRUE" ]; then
  gunicorn --bind 0.0.0.0:8000 -k gevent -w ${worker} project.wsgi
else
  python manage.py runserver 0.0.0.0:${port}
fi
