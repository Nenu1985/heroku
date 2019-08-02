release: python manage.py makemigrations
release: python manage.py migrate
release: python manage.py loaddata course.json
web: gunicorn gettingstarted.wsgi --log-file -

