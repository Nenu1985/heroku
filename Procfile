release: python manage.py makemigrations
release: python manage.py migrate
release: python manage.py loaddata db.json
web: gunicorn gettingstarted.wsgi --log-file -
