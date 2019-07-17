from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


####
# solved proble####m:
# https://stackoverflow.com/questions/45744992/celery-raises-valueerror-not-enough-values-to-unpack
# add a string to this file: 'os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
# AND start:
# --->'celery -A gettingstarted worker -l info -E'
# celery -A gettingstarted worker --loglevel=info
#
# INSTALL REDIS:
# sudo apt-get install redis-server  # - install
# sudo systemctl enable redis-server.service  #  launch and on the boot
# sudo systemctl restart redis-server.service  # restart

# Test connection:
# redis-cli
#
# 127.0.0.1:6379> ping
# PONG

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gettingstarted.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')  # only use on Windows!

app = Celery('gettingstarted')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
# app.autodiscover_tasks(packages='gettingstarted')

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

