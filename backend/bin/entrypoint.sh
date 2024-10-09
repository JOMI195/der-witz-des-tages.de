#!/bin/sh

echo "Migrating the database..."
python manage.py makemigrations
python manage.py migrate


# echo "Translating content..."
# django-admin makemessages
# django-admin compilemessages


echo "Collecting static files..."
python manage.py collectstatic --noinput

if [ "$DJANGO_SUPERUSER_EMAIL" ]
then
echo "Creating superuser..."
python manage.py createsuperuser --noinput
fi

if [ -n "$PRODUCTION" ]; then
  if [ "$PRODUCTION" = "True" ]; then
    echo "PRODUCTION is set to 'True', skipping adding fixtures."
  else
    echo "Adding preset jokes..."
    python manage.py load_jokes

    echo "Adding preset newsletter recievers..."
    python manage.py load_recievers
  fi
else
  echo "PRODUCTION is not set, skipping adding fixtures."
fi

exec "$@"