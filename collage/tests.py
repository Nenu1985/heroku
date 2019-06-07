
from django.test import TestCase, Client
from collage.models import Collage, PhotoSize
from django.db.utils import IntegrityError
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, Client, RequestFactory
from django.db.utils import IntegrityError
from django.urls import reverse
import flickrapi
from django.conf import settings
import requests
from os.path import basename
from tempfile import TemporaryFile
from django.db import transaction
from django.utils import timezone
from urllib.parse import urlsplit
from django.core.files import File
from django.shortcuts import get_list_or_404, get_object_or_404


from .models import Photo
from collage.models import Collage, PhotoSize
from django.urls import reverse
# >>> from django.test.utils import setup_test_environment
# >>> setup_test_environment()
# Create your tests here.


# tests.py

# Test Flickr API: get urls and download images by the urls via requests lib
class FlickrTest(TestCase):

    def test_flickr_keys(self):
        self.assertEqual(settings.GLOBAL_SETTINGS['FLICKR_PUBLIC'],
                         '1f9874c1a8ea5a85acfd419dd0c2c7e1',
                         'Flickr public key is wrong')

        self.assertEqual(settings.GLOBAL_SETTINGS['FLICKR_SECRET'],
                         '67de04d2825fd397',
                         'Flickr secret key is wrong')

    def test_flickr_api(self):
        flickr = flickrapi.FlickrAPI(
            settings.GLOBAL_SETTINGS['FLICKR_PUBLIC'],
            settings.GLOBAL_SETTINGS['FLICKR_SECRET'],
        )

        extras = 'url_q'  # 150 pixels per side and above

        photos = flickr.walk(text='man',
                             per_page=5,
                             extras=extras
                             )
        retrieved_url = ''
        for i, photo in enumerate(photos):
            url = photo.get(extras, 'no url')
            if url != 'no url':  # if url is empty - pass it and increment photo number
                retrieved_url = url
                break
        self.assertTrue(retrieved_url, 'Flickr didn\'t find any url')

        # download a file by url with chunks and create a Photo in db
        with TemporaryFile() as tf:
            r = requests.get(retrieved_url, stream=True)
            for chunk in r.iter_content(chunk_size=4096):
                tf.write(chunk)

            tf.seek(0)
            with transaction.atomic():
                photo = Photo()
                photo.photo_url = retrieved_url
                photo.date = timezone.now()
                photo.img_field.save(basename(urlsplit(retrieved_url).path), File(tf))

        self.assertTrue(photo, 'Photo object didn\'t create')

        self.assertTrue(photo.img_field.url, 'Photo object doesn\'t have a photo url')

        self.assertEqual(photo.photo_url, retrieved_url)