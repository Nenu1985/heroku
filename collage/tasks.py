# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
from gettingstarted.celery import app
from .models import Collage, ProgressRecorder, face_detect_cut_first_face, Photo
from time import sleep
from django.utils import timezone
from django.db import transaction
import aiohttp
import asyncio
import aiofiles
import os
import time
from decimal import Decimal
import threading, concurrent.futures
from os.path import basename
from urllib.parse import urlsplit
from django.conf import settings
from itertools import repeat
import logging

logger = logging.getLogger('django.server')

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task(bind=True)
def launch_processing(self, collage_id):

    # instance for progressbar status update
    progress_recorder = ProgressRecorder(self)
    print('launch_processing: start!')
    # collage instance
    collage = Collage.objects.get(id=collage_id)

    # get photo urls by flickr api
    photo_urls = collage.get_photos_urls()
    #photo_urls = [8,8,8,8,8,8,8,8]
    print('launch_processing: urls retrieved!')
    # download, store and return photos
    for i, url in enumerate(photo_urls):
        new_photo = collage.download_photos_by_url(url)
        with transaction.atomic():
            new_photo.save()
            collage.photos.add(new_photo)
            progress_recorder.set_progress(collage.photos.count(), collage.photo_number)

    progress_recorder.set_progress(collage.photo_number, collage.photo_number)


    return "Collage created. Id = {}, " \
           "Date = {}".format(collage.id,
                              collage.create_date.strftime("%d %b %Y %H:%M:%S"))


@app.task
def test_long_task():
    sleep(3)
    return 'Slept ok'


@shared_task
def test_long_task2():
    sleep(4)
    return 'Slept ok'


@shared_task(bind=True)
def my_task(self, seconds):
    progress_recorder = ProgressRecorder(self)
    for i in range(seconds):
        time.sleep(1)
        progress_recorder.set_progress(i + 1, seconds)
    return 'done'


@app.task(bind=True)
def my_task2(self):
    time.sleep(1)
    return 'my_task3: {}'.format(self.request.id)


async def image_dowload(url):
    img_location = basename(urlsplit(url).path)
    photo = Photo.objects.filter(img_location=img_location)
    if not photo:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    # f = await aiofiles.open('./image/{}.jpg'.format(file_name), mode='wb')
                    # (path=os.path.join(settings.MEDIA_ROOT, 'upload_collage_photos'))
                    f = await aiofiles.open(
                        os.path.join(settings.UPLOAD_ASYNC, img_location), mode='wb')
                    await f.write(await resp.read())
                    await f.close()

                    with transaction.atomic():
                        new_photo = Photo()
                        new_photo.photo_url = url
                        new_photo.date = timezone.now()
                        new_photo.img_location = img_location
                        new_photo.save()
                    # size = os.path.getsize('./image/{}.jpg'.format(file_name))
                    # print(f'image {file_name} downloaded. Size = {size/1024}kB. Time = {time.time() - start}')
                    # await asyncio.sleep(0.2)
                    return new_photo.id
    else:
        return photo[0].id



def query_processing(executor, img_urls, progress_recorder=None, loop=None):

    print(f'--ASYNC-IO---, pr_id={progress_recorder.id}')
    start = time.time()
    # Way1 to create coroutines
    futures_download_imgs = [image_dowload(url) for i, url in enumerate(img_urls)]

    collage = Collage.objects.get(id=progress_recorder.collage_id)
    logger.info(f'TASKS PROCESSING: thread={threading.current_thread().ident}')
    # loop.set_debug(True)
    while progress_recorder.percent < 100:
        finished, unfinished = loop.run_until_complete(asyncio.wait(futures_download_imgs,
                                                                     return_when=asyncio.FIRST_COMPLETED))
        futures_download_imgs = unfinished

        for result in finished:
            photo = Photo.objects.get(id=result.result())
            collage.photos.add(photo)

        with transaction.atomic():
            progress_recorder.set_progress(len(img_urls) - len(unfinished), len(img_urls))
            progress_recorder.save()
        logger.info(f'TASKS PROCESSING: thread={threading.current_thread().ident}, PR={progress_recorder}')
        # print(f'TASKS PROCESSING: thread={threading.current_thread().ident}, PR={progress_recorder}')

    # ---DOWNLOADING HAS FINISHED. PROCESSING STARTS! ---- #
    logger.info(f'TASKS PROCESSING: DOWNLOADED: thread={threading.current_thread().ident}, PR={progress_recorder}')
    # reset progress state
    with transaction.atomic():
        progress_recorder.proc_name = 'Processing'
        progress_recorder.set_progress(0, len(img_urls))
        progress_recorder.save()

    # define futures for blocking routines
    futures_to_img_process = [
        loop.run_in_executor(executor, face_detect_cut_first_face, photo, collage.photo_size)
        for photo in list(collage.photos.all())
    ]
    # processing
    while progress_recorder.percent < 100:
        finished, unfinished = loop.run_until_complete(asyncio.wait(futures_to_img_process,
                                                                     return_when=asyncio.FIRST_COMPLETED))
        futures_to_img_process = unfinished

        with transaction.atomic():
            progress_recorder.set_progress(len(img_urls) - len(unfinished), len(img_urls))
            progress_recorder.save()

            logger.info(f'TASKS PROCESSING: thread={threading.current_thread().ident}, PR {progress_recorder}')
            # print(f'TASKS PROCESSING: thread={threading.current_thraead().ident}, PR={progress_recorder}')
    logger.info(f'TASK PROCESSED!: {progress_recorder}')
    # print(f'All images download in  {time.time() - start}. P_percent={progress_recorder.percent}')
    collage.generate_collage()
    progress_recorder.proc_name = 'Collage has generated!'
    logger.info(f'TASK COLLAGE GENERATED!: {progress_recorder}')
    progress_recorder.save()

def start_daemon_thread(progress_recorder_id, urls):

    logger.debug('TASKS: starting thread to download and process images')

    progress_recorder = ProgressRecorder.objects.get(id=progress_recorder_id)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count(),
    )
    try:
        a = threading.Thread(target=query_processing,
                             args=(executor, urls, progress_recorder, loop,))
        a.start()
        logger.info(f'TASKS: thread started! idend = {a.ident}')
        # progress_recorder.thread_id = a.ident
        progress_recorder.save()

    except Exception as e:
        print(f'Error: {e}')
        logger.info(f'Eror:{e}')

    return a.ident