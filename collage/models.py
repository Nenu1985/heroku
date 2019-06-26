from django.db import models
from django.utils import timezone
import urllib
import requests
import datetime
import flickrapi
from django.conf import settings
from django.core.cache import cache
from tempfile import TemporaryFile
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
from urllib.parse import urlsplit
from os.path import basename
import cv2
import os, platform
import numpy as np
import uuid, logging
from model_utils import Choices
from django.db import transaction
from decimal import Decimal

logger = logging.getLogger('django.models')

class PhotoSize(models.Model):
    size = models.IntegerField(default=128)

    def __str__(self):
        return str(self.size)

class CutPhoto(models.Model):
    #photo_src = models.ForeignKey(Photo, on_delete=models.CASCADE, unique=True)
    # photo_src = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name='cut_photos')
    TYPE_CHOICES = Choices(         # 1 - db value, 2 - code value, 3 - human readable value
        (0, 'contour', 'Objs rounded with rect'),  # ex: in db 0; from code TYPE_CHOICES.contour; in admin 'Objs rounded ...'
        (128, 'r128', 'Resized to 128'),
        (256, 'r256', 'Resized to 256'),
        (1, 'cut', 'cut'),
    )
    img_field = models.ImageField(upload_to='cut_collage_photos')
    img_location = models.FilePathField(path=settings.UPLOAD_ASYNC)
    date = models.DateTimeField(auto_now_add=True)
    photo_type = models.IntegerField(default=1, choices=TYPE_CHOICES)
    size = models.IntegerField(default=128)

    def save_img_to_field(self):
        if not self.img_field:
            with open(os.path.join(settings.UPLOAD_ASYNC, self.img_location), 'rb') as file:
                self.img_field.save(self.img_location, file)

    def delete(self, using=None, keep_parents=False):
        path = os.path.join(settings.UPLOAD_ASYNC, self.img_location)
        if os.path.isfile(path):
            os.remove(path)
        if self.img_field and os.path.isfile(self.img_field.path):
            os.remove(self.img_field.path)

        super().delete(using=using, keep_parents=keep_parents, )



class Photo(models.Model):
    photo_url = models.URLField(default='tutorial:index')
    img_field = models.ImageField(upload_to='upload_collage_photos', blank=True)
    img_location = models.FilePathField(path=settings.UPLOAD_ASYNC)
    date = models.DateTimeField(auto_now_add=True)
    cut_photos = models.ManyToManyField(CutPhoto, related_name='photos', blank=True)

    def resize(self, width):


        if width == 256:
            cut_photos_256 = self.cut_photos.filter(photo_type=CutPhoto.TYPE_CHOICES.r256)
            if cut_photos_256:
                return cut_photos_256[0]


        if width == 128:
            cut_photos_128 = self.cut_photos.filter(photo_type=CutPhoto.TYPE_CHOICES.r128)
            if cut_photos_128:
                return cut_photos_128[0]

        if width != 128 or width != 256:
            logger.info(f'MODEL RESIZE: Width doesn\'t match requirements')

        self.save_img_to_field()

        src_img = cv2.imread(self.img_field.path)

        if not src_img.any():
            logger.info(f'MODEL PHOTO RESIZE: There is empty image with path in {self}')

        frame_width = src_img.shape[1]

        # adjust src_img shape to shape that not less than required size
        # newimg = cv2.resize(oriimg, (int(newX), int(newY)))
        if frame_width != width:  # height
            scale_coef = width / frame_width
            src_img = cv2.resize(src_img, (int(src_img.shape[1] * scale_coef), int(src_img.shape[0] * scale_coef)))

        with transaction.atomic():
            cut_photo = CutPhoto()
            cut_photo.photo_type = CutPhoto.TYPE_CHOICES.r128 if width == 128 else CutPhoto.TYPE_CHOICES.r256
            Collage.save_mat_to_image_field(src_img, cut_photo.img_field)
            cut_photo.save()
            self.cut_photos.add(cut_photo)

        return cut_photo

    def save_img_to_field(self):
        if not self.img_field:
            with open(os.path.join(settings.UPLOAD_ASYNC, self.img_location), 'rb') as file:
                self.img_field.save(self.img_location, file)

    def __str__(self):
        return f'url:{self.photo_url}; loc:{self.img_location}; date:{self.date.time()};'

    def delete(self, using=None, keep_parents=False):
        path = os.path.join(settings.UPLOAD_ASYNC, self.img_location)
        if os.path.isfile(path):
            os.remove(path)
        if self.img_field and os.path.isfile(self.img_field.path):
            os.remove(self.img_field.path)
        super().delete(using=using, keep_parents=keep_parents, )

    @staticmethod
    def download_photos_by_url(photo_url):
        """
        Download a photo by url, save it to DB in photo model, return Photo instance
        :param photo_url: url photo(img) to download
        :return: photo model instance
        """
        # file_name = f'collage\photo\\src{str(num)}.jpg'
        try:
            check_photo_exists = Photo.objects.filter(photo_url=photo_url).first()
            if check_photo_exists:
                return Photo.objects.filter(photo_url=photo_url).first()
            else:
                with TemporaryFile() as tf:
                    r = requests.get(photo_url, stream=True)
                    for chunk in r.iter_content(chunk_size=4096):
                        tf.write(chunk)

                    tf.seek(0)
                    with transaction.atomic():
                        photo = Photo()
                        photo.photo_url = photo_url
                        photo.date = timezone.now()
                        photo.img_field.save(basename(urlsplit(photo_url).path), File(tf), save=False)
                        photo.save()

                return photo
        except Exception as e:
            print('download_photos_by_url' + e)
            return None

    def face_detect_contour(self):

        exists = self.cut_photos.filter(photo_type=CutPhoto.TYPE_CHOICES.contour)

        if exists:
            return exists[0]

        src_img = cv2.imread(os.path.join(settings.UPLOAD_ASYNC, self.img_location))
        if not src_img.any():
            logger.info(f'MODEL: There is empty image with path in {self}')

        processing_img = src_img.copy()

        # get classifier
        # face_cascade = cv2.CascadeClassifier("collage\\haar\\haarcascade_frontalface_default.xml")  # Win style
        face_cascade = cv2.CascadeClassifier("./collage/haar/haarcascade_frontalface_default.xml")  # Ubuntu style

        # face detector
        gray = cv2.cvtColor(processing_img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
        for (x, y, w, h) in faces:
            processing_img = cv2.rectangle(processing_img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        if not list(faces):
            # draw a red cross:
            cv2.line(processing_img, (5, 5), (15, 15), (0, 0, 255), thickness=2)
            cv2.line(processing_img, (15, 5), (5, 15), (0, 0, 255), thickness=2)
        else:
            cv2.line(processing_img, (5, 5), (7, 14), (0, 255, 0), thickness=2)
            cv2.line(processing_img, (7, 14), (14, 5), (0, 255, 0), thickness=2)
        # roi = Collage.get_roi(int(frame_width / 2), int(frame_height / 2), frame_width, frame_height, iw_h)
        # face_cascade = cv2.CascadeClassifier("collage\\haar\\haarcascade_frontalface_default.xml")
        # out_small_image = src_img[roi[1] - iw_h:roi[1] + iw_h - 1,
        #                   roi[0] - iw_h:roi[0] + iw_h - 1].copy()
        with transaction.atomic():
            cut_photo = CutPhoto()
            # cut_photo.photo_src = photo_src
            cut_photo.photo_type = CutPhoto.TYPE_CHOICES.contour
            Collage.save_mat_to_image_field(processing_img, cut_photo.img_field)
            cut_photo.save()
            self.cut_photos.add(cut_photo)

        return cut_photo

class Collage(models.Model):

    SIZE_CHOICES = Choices(
        (128, '128', '128'),  # 1 - db value, 2 - code value, 3 - human readable value
        (256, '256', '256'),
        (512, '512', '512'),
    )
    photo_number = models.IntegerField(default=10)
    cols_number = models.IntegerField(default=5)
    create_date = models.DateTimeField(auto_now_add=True)
    photo_tag = models.CharField(max_length=30, default='women')
    # photo_size = models.ForeignKey(PhotoSize, on_delete=models.CASCADE, blank=True)
    photos = models.ManyToManyField(Photo, blank=True, related_name="collages")
    photo_size = models.IntegerField(default=128, choices=SIZE_CHOICES)
    final_img = models.ImageField(upload_to='collages', blank=True)

    def delete(self, using=None, keep_parents=False):
        if self.final_img:
            if os.path.isfile(self.final_img.path):
                os.remove(self.final_img.path)
        super().delete(using=using, keep_parents=keep_parents, )

    class Meta:
        ordering = ('-create_date',)

    def __str__(self):
        return f'Collage {self.id} N={self.photo_number} Cols={self.cols_number} size={self.photo_size}' \
               f'N of photo={len(self.photos.all())}'

    def download_photos_by_url(self, photo_url):
        """
        Download a photo by url, save it to DB in photo model, return Photo instance
        :param photo_url: url photo(img) to download
        :return: photo model instance
        """
        # file_name = f'collage\photo\\src{str(num)}.jpg'
        try:
            check_photo_exists = Photo.objects.filter(photo_url=photo_url).first()
            if check_photo_exists:
                collage_inst = check_photo_exists.collage_set.filter(id=self.id)
                if collage_inst and collage_inst.photo_size == self.photo_size:
                    return Photo.objects.filter(photo_url=photo_url).first()
        except Exception as e:
            print('download_photos_by_url' + e)
        finally:

            with TemporaryFile() as tf:
                r = requests.get(photo_url, stream=True)
                for chunk in r.iter_content(chunk_size=4096):
                    tf.write(chunk)

                tf.seek(0)
                with transaction.atomic():
                    photo = Photo()
                    photo.photo_url = photo_url
                    photo.date = timezone.now()
                    photo.img_field.save(basename(urlsplit(photo_url).path), File(tf))

            return photo


    @classmethod
    def get_roi(cls, x_c: int, y_c: int, i_w: int, i_h: int, iw_h: int):
        """
        find ROI of image
        :param x_c: center X coord of ROI, pixels (int)
        :param y_c: center Y coord of ROI, pixels (int)
        :param i_w: input img width
        :param i_h: input img height
        :param iw_h: half of output img with and height
        :return: tuple(outxc, outyc)
        """
        outx_c = x_c
        outy_c = y_c

        if x_c + iw_h > i_w and outx_c - (iw_h - (i_w - x_c)) > iw_h:
            outx_c -= iw_h - (i_w - x_c)
        elif x_c - iw_h < 0 and outx_c + (iw_h - x_c) < i_w:
            outx_c += iw_h - x_c

        if y_c + iw_h > i_h and outy_c - (iw_h - (i_h - y_c)) > iw_h:
            outy_c -= iw_h - (i_h - y_c)
        elif y_c - iw_h < 0 and outy_c + (iw_h - y_c) < i_w:
            outy_c += iw_h - y_c

        assert outx_c >= iw_h, 'outx_c {} + iw_h {}'.format(outx_c, iw_h)
        assert outy_c >= iw_h, 'outy_c {} + iw_h {}'.format(outy_c, iw_h)

        return outx_c, outy_c


    @classmethod
    def save_mat_to_image_field(cls, image, img_field):

        file_path = settings.MEDIA_ROOT + '\\_temp.jpg'  # Win style
        file_path = settings.MEDIA_ROOT + '/_temp.jpg'  # Ubuntu style
        cv2.imwrite(file_path, image)

        with open(file_path, 'rb') as photo_file:
            f_name = uuid.uuid4().hex[:6]
            f_django = File(photo_file)
            img_field.save(
                f_name,
                f_django,
            )

        try:
            os.remove(file_path)
        except Exception:
            print(Exception)


    def generate_collage(self):
        photos = self.photos.all()

        rows = int(self.photo_number / self.cols_number)
        size = self.photo_size

        big_img = np.zeros(
            (size * rows, size * self.cols_number, 3),
            np.uint8
        )

        imgs = []

        for photo in photos:
            cut_photos = photo.cut_photos.filter(photo_type=CutPhoto.TYPE_CHOICES.cut)
            for cut_photo in cut_photos:

                img = cv2.imread(os.path.join(settings.UPLOAD_ASYNC, cut_photo.img_location))
                if img.shape[0] == (self.photo_size - 1) and cut_photo.size == self.photo_size:
                    imgs.append(img)

            if not imgs:
                logger.info(f'MODELS: There is no cut_photo in photo! {self}')
                img = np.zeros((self.photo_size - 1, self.photo_size - 1, 3), np.uint8)  # empty image
                img[:, :, 2] = 255  # red color
                imgs.append(img)

        try:
            for row in range(rows):
                for col in range(self.cols_number):
                    big_img[row * size: row * size + size - 1,
                            col * size: col * size + size - 1,
                            :] = imgs[row*self.cols_number + col]
        except Exception as e:
            print(e)


        Collage.save_mat_to_image_field(big_img, self.final_img)


    #url_c: URL of medium 800, 800 on longest size image
    #url_m: URL of small, medium size image
    #url_n: URL of small, 320 on longest side size image
    #url_o: URL of original size image
    #url_q: URL of large square 150x150 size image
    #url_s: URL of small suqare 75x75 size image
    #url_sq: URL of square size image
    #url_t: URL of thumbnail, 100 on longest side size image

def get_photos_urls(count, tag, size):
    flickr = flickrapi.FlickrAPI(
        settings.GLOBAL_SETTINGS['FLICKR_PUBLIC'],
        settings.GLOBAL_SETTINGS['FLICKR_SECRET'],
        cache=True
    )
    extras = "url_s"        # 75 pixels per side and above
    if size == 128:
        extras = "url_q"    # 150 pixels per side and above
    else:
        extras = "url_n"    # 320 pixels per side and above

    photos = flickr.walk(text=tag,
                         per_page=int(count*1.2),  # may be you can try different numbers..
                         extras=extras
                         )
    urls = []
    num_of_photos = count - 1
    for i, photo in enumerate(photos):
        url = photo.get(extras, 'no url')
        if url != 'no url':  # if url is empty - pass it and increment photo number
            urls.append(url)
        else:
            num_of_photos += 1
        if i >= num_of_photos:
            break
    return urls


def download_photos_by_url(photo_url):
    """
    Download a photo by url, save it to DB in photo model, return Photo instance
    :param photo_url: url photo(img) to download
    :return: photo model instance
    """
    # file_name = f'collage\photo\\src{str(num)}.jpg'
    try:
        check_photo_exists = Photo.objects.filter(photo_url=photo_url).first()
        if check_photo_exists:
            return Photo.objects.filter(photo_url=photo_url).first()

    except Exception as e:
        print('download_photos_by_url' + e)

    with TemporaryFile() as tf:
        r = requests.get(photo_url, stream=True)
        for chunk in r.iter_content(chunk_size=4096):
            tf.write(chunk)

        tf.seek(0)
        with transaction.atomic():
            photo = Photo()
            photo.photo_url = photo_url
            photo.date = timezone.now()
            photo.img_field.save(basename(urlsplit(photo_url).path), File(tf))

        return photo

def get_roi(x_c: int, y_c: int, i_w: int, i_h: int, iw_h: int):
    """
    find ROI of image
    :param x_c: center X coord of ROI, pixels (int)
    :param y_c: center Y coord of ROI, pixels (int)
    :param i_w: input img width
    :param i_h: input img height
    :param iw_h: half of output img with and height
    :return: tuple(outxc, outyc)
    """
    outx_c = x_c
    outy_c = y_c

    if x_c + iw_h > i_w and outx_c - (iw_h - (i_w - x_c)) > iw_h:
        outx_c -= iw_h - (i_w - x_c)
    elif x_c - iw_h < 0 and outx_c + (iw_h - x_c) < i_w:
        outx_c += iw_h - x_c

    if y_c + iw_h > i_h and outy_c - (iw_h - (i_h - y_c)) > iw_h:
        outy_c -= iw_h - (i_h - y_c)
    elif y_c - iw_h < 0 and outy_c + (iw_h - y_c) < i_w:
        outy_c += iw_h - y_c

    assert outx_c >= iw_h, 'outx_c {} + iw_h {}'.format(outx_c, iw_h)
    assert outy_c >= iw_h, 'outy_c {} + iw_h {}'.format(outy_c, iw_h)

    return outx_c, outy_c


def face_detect_cut_first_face(photo, photo_size):

    # log = logging.getLogger('file: ({})'.format(inp_im_file_name))
    # log.info('running')
    inp_im_file_name = os.path.join(settings.UPLOAD_ASYNC, photo.img_location)
    output_im_file_name = inp_im_file_name[:-4] + '_processed.jpg'
    img_location = basename(urlsplit(output_im_file_name).path)

    cut_photo_exists = CutPhoto.objects.filter(img_location=img_location)\
                                       .filter(photo_type=CutPhoto.TYPE_CHOICES.cut)\
                                       .filter(size=photo_size)


    if cut_photo_exists:
        cut_photo_exists = cut_photo_exists[0]
        logger.info(f'MODELS: Cut photo exists: {cut_photo_exists}')
        return 1

    src_img = cv2.imread(inp_im_file_name)


# adjust src_img shape to shape that not less than required size
    # newimg = cv2.resize(oriimg, (int(newX), int(newY)))

    processing_img = src_img.copy()
    frame_height = src_img.shape[0]
    frame_width = src_img.shape[1]

    if frame_height < photo_size:
        coef_h = photo_size / frame_height
        src_img = cv2.resize(src_img, (int(frame_width * coef_h), int( frame_height * coef_h)))

    frame_height = src_img.shape[0]
    frame_width = src_img.shape[1]
    if frame_width < photo_size:
        coef_w = photo_size / frame_width
        src_img = cv2.resize(src_img, (int(frame_width * coef_w), int( frame_height * coef_w)))
    # resize source image for better processing
    in_height = 500  # initial image height for good face detect
    in_width = int((frame_width / frame_height) * in_height)
    processing_img = cv2.resize(processing_img, (in_width, in_height))

    # get classifier
    # face_cascade = cv2.CascadeClassifier("collage\\haar\\haarcascade_frontalface_default.xml")  # Win style
    face_cascade = cv2.CascadeClassifier("./collage/haar/haarcascade_frontalface_default.xml")  # Ubuntu style
    # face detector
    gray = cv2.cvtColor(processing_img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
    roi = (0, 0)
    iw_h = photo_size >> 1  # half of required size


    # choose the first face, find center of rect
    if not list(faces):  # if no face detected select the middle of the picture
        roi = get_roi(int(frame_width / 2), int(frame_height / 2),
                      int(frame_width), int(frame_height), iw_h)

    else:  # faces are detected, select one of them
        x_center = int((faces[0][0] + faces[0][2] / 2) * (frame_width / in_width))
        y_center = int((faces[0][1] + faces[0][3] / 2) * (frame_height / in_height))
        roi = get_roi(x_center, y_center, frame_width, frame_height, iw_h)

        # cv2.resize(src_img, fx=scale_coef, fy=scale_coef)

    out_small_image = src_img[roi[1] - iw_h:roi[1] + iw_h - 1,
                      roi[0] - iw_h:roi[0] + iw_h - 1].copy()

    if not list(faces):
        # draw a red cross:
        cv2.line(out_small_image, (5, 5), (15, 15), (0, 0, 255), thickness=2)
        cv2.line(out_small_image, (15, 5), (5, 15), (0, 0, 255), thickness=2)
    else:
        cv2.line(out_small_image, (5, 5), (7, 14), (0, 255, 0), thickness=2)
        cv2.line(out_small_image, (7, 14), (14, 5), (0, 255, 0), thickness=2)

    cv2.imwrite(output_im_file_name, out_small_image)

    with transaction.atomic():
        cut_photo = CutPhoto()
        cut_photo.img_location = img_location
        cut_photo.photo_type = CutPhoto.TYPE_CHOICES.cut
        cut_photo.size = photo_size
        cut_photo.save()

        photo.cut_photos.add(cut_photo)
        photo.save()

    logger.info(f'MODELS: Cut photo created: {cut_photo}')
    # time.sleep(0.2)
    return cut_photo


def get_system_info():
    cpus = os.cpu_count()
    num_of_collages = len(Collage.objects.all())
    files = [f for f in os.listdir(settings.UPLOAD_ASYNC)
                 if os.path.isfile(os.path.join(settings.UPLOAD_ASYNC, f))]

    files_size = sum(os.path.getsize(os.path.join(settings.UPLOAD_ASYNC, f)) for f in files)
    system_info = {
        'cpus': cpus,
        'n_of_collages': num_of_collages,
        'files_size': f'{files_size/1024:.1f} kB',
        'os': platform.uname(),
    }
    return system_info


class ProgressRecorder(models.Model):

    current = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    percent = models.IntegerField(default=0)
    proc_name = models.CharField(max_length=30, default='downloading')
    collage_id = models.IntegerField(default=0)
    # thread_id = models.F(default=0)

    def set_progress(self, current, total):
        self.current = current
        self.total = total
        self.percent = int(round((Decimal(current) / Decimal(total)) * Decimal(100), 2) if total > 0 else 0)

    def __str__(self):
        return f'id={self.id}; current={self.current}; {self.proc_name} ' \
               f'{self.percent}%; collage={self.collage_id};'
