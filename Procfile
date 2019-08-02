release: python manage.py makemigrations
release: python manage.py migrate
release: python loaddata course.json
web: gunicorn gettingstarted.wsgi --log-file -

