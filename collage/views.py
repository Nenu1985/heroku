from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from collage.models import Photo, CutPhoto, Collage
from .forms import InputUrlFrom, CollageCreateForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404
from .tasks import my_task, start_daemon_thread, image_dowload
from collage.models import get_photos_urls, download_photos_by_url, ProgressRecorder, get_system_info, face_detect_cut_first_face
from django.conf import settings
from django.views.decorators.csrf import csrf_protect

from gettingstarted.celery import app
import json, logging, os, asyncio

logger = logging.getLogger('django.view')


# Create your views here.
def show_image(request, img_id):
    img = get_object_or_404(Photo, id=img_id)
    if not img.img_field:
        img.save_img_to_field()

    cut_photos = img.cut_photos.all()
    for photo in cut_photos:
        if not photo.img_field:
            photo.save_img_to_field()

    # Create resized photos
    for photo in Photo.objects.all():
        photo.resize(128)

    cut_resized_photos = CutPhoto.objects.filter(photo_type=CutPhoto.TYPE_CHOICES.r128)

    return render(request, 'collage/image.html', {'photo': img,
                                                  'cut_photos': cut_photos,
                                                  'path': settings.UPLOAD_ASYNC,
                                                  'cut_resized_photos': cut_resized_photos,})


@csrf_protect
def main(request):
    if request.method == 'GET':

        context = {
            'form': InputUrlFrom(),
        }
        return render(request, 'collage/url_form.html', context)
    elif request.method == 'POST':
        input_form = InputUrlFrom(request.POST)
        url = input_form['url_to_img'].value()
        # url = http://www.funlava.com/wp-content/uploads/2016/04/Beautiful-Girls-Images-2.jpg
        # photo_instance = Photo(photo_url=url)


        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        photo_id = loop.run_until_complete(image_dowload(url))
        photo = get_object_or_404(Photo, id=photo_id)
        logger.info(f'VIEW:MAIN: {photo} is downloaded!')

        photo.face_detect_contour()
        face_detect_cut_first_face(photo, 256)

        return redirect(reverse('collage:show-image', kwargs={'img_id': photo_id,}))


#
def get_photo(request, collage_id):
    #     collage = Collage.objects.all().filter(id=collage_id).first()
    #     urls = collage.get_photos_urls()
    #
    #     for i, url in enumerate(urls):
    #         collage.download_photos_by_url(url, i)
    #
    #     urls_photos = list(zip(urls, range(len(urls))))
    #     context = {
    #         'urls': urls,
    #         'collage': collage,
    #         'urls_photos': urls_photos
    #     }
    return HttpResponse('get_photo')


def collage_input_form(request):
    if request.method == 'POST':
        if "query_type" in request.POST and request.POST["query_type"]:
            query_type = request.POST["query_type"]
        else:
            query_type = 'none'

        if query_type == 'collage_launch':
            collage_input_form = CollageCreateForm(request.POST)
            if collage_input_form.is_valid():
                collage = collage_input_form.save(commit=False)
            else:
                return HttpResponse(status=405)

            collage.save()

            logger.info(f'VIEW: collage_launch. Created collage id = {collage.id}')

            urls = get_photos_urls(collage.photo_number, collage.photo_tag, collage.photo_size)

            # photos = []
            # local_photo_urls = []
            # for i, url in enumerate(urls):
            #     photo = download_photos_by_url(url)
            #     photos.append(photo)
            #     local_photo_urls.append(photo.img_field.url)

            progress_recorder = ProgressRecorder(collage_id=collage.id)

            progress_recorder.save()

            thread_id = start_daemon_thread(progress_recorder.id, urls)
            logger.info(f'VIEW: collage_launch. Thread launched with ident = {thread_id}')
            #
            # celery_status = get_celery_worker_status()
            #
            # if celery_status.get('ERROR', None):
            #     return HttpResponse(celery_status.get('ERROR'))
            # else:
            #     print('Celery is OK!')
            #
            # res = launch_processing.delay(collage.pk)
            # # res = my_task.delay(10);
            # # launch_processing(collage.pk)
            # response = reverse('celery_progress:task_status', kwargs={'task_id': res.task_id})
            # response = reverse('celery_progress:task_status', kwargs={'task_id': 0})

            # 13.06.2019 - simple photo view
            # return JsonResponse(local_photo_urls, safe=False)
            response = {
                'task_id': progress_recorder.id,
                'success': True,
                'message': 'Emploee added successfully by ajax',
                # 'progress_obj': progress_obj,
            }
            return HttpResponse(json.dumps(response))
        # -- AJAX PB POLLS ----#
        elif query_type == 'poll':
            progress_id = request.POST.get('task_id')
            progress_recorder = ProgressRecorder.objects.get(id=progress_id)

            logger.info(f"VIEW: Ajax thread status poll. Progress = {progress_recorder}. Time {timezone.now().time()}")

            # print(f'Ajax poll status: {progress_recorder.percent}, {progress_recorder.proc_name}')
            context = {
                'progress': progress_recorder.percent,
                'proc_name': progress_recorder.proc_name,
            }
            return HttpResponse(json.dumps(context))
        elif query_type == 'get_collage':
            progress_id = request.POST['task_id']
            progress_recorder = get_object_or_404(ProgressRecorder, id=progress_id)
            collage = get_object_or_404(Collage, id=progress_recorder.collage_id)
            return HttpResponse(collage.final_img.url)
    else:

        context = {
            'form': CollageCreateForm(),
            'system_info': get_system_info(),
        }
        return render(request, 'collage/collage_form.html', context)
    return HttpResponse('Hello!')
# def collage_input(request):
#     if request.method == 'GET':
#
#         context = {
#             'collage_input': CollageInputForm(),
#         }
#         return render(request, 'collage/input.html', context)
#     elif request.method == 'POST':
#         if request.is_ajax() and request.method == 'POST':
#
#             if "query_type" in request.POST and request.POST["query_type"]:
#                 query_type = request.POST["query_type"]
#             else:
#                 query_type = 'none'
#
#             if query_type == 'poll':
#                 # When images downloaded!
#                 collage = Collage.objects.filter(user=request.user).latest('id')
#                 collage.get_cv2_images()
#                 collage.generate_collage()
#
#                 return HttpResponse(collage.final_img.url)
#
#             elif query_type == 'collage_launch':
#                 collage_input_form = CollageInputForm(request.POST)
#                 if collage_input_form.is_valid():
#                     collage = collage_input_form.save(commit=False)
#                 else:
#                     return HttpResponse(status=405)
#
#                 collage.user = request.user
#                 collage.save()
#
#                 celery_status = get_celery_worker_status()
#
#                 if celery_status.get('ERROR', None):
#                     return HttpResponse(celery_status.get('ERROR'))
#                 else:
#                     print('Celery is OK!')
#
#                 # res = launch_processing.delay(collage.pk)
#                 res = my_task.delay(10);
#                 # launch_processing(collage.pk)
#                 response = reverse('celery_progress:task_status', kwargs={'task_id': res.task_id})
#                 # response = reverse('celery_progress:task_status', kwargs={'task_id': 0})
#                 return HttpResponse(response)
#
#             elif query_type == 'progress_launch':
#                 result = my_task.delay(10)
#                 response = reverse('celery_progress:task_status', kwargs={'task_id': result.task_id})
#                 return HttpResponse(response)
#             else:
#                 return HttpResponse(status=405)
#         else:
#             return HttpResponse(status=405)
#     else:
#         return HttpResponse(status=405)

def get_celery_worker_status():

    ERROR_KEY = "ERROR"
    try:
        insp = app.control.inspect()

        d = insp.stats()
        if not d:
            d = { ERROR_KEY: 'No running Celery workers were found.' }
    except IOError as e:
        from errno import errorcode
        msg = "Error connecting to the backend: " + str(e)
        if len(e.args) > 0 and errorcode.get(e.args[0]) == 'ECONNREFUSED':
            msg += ' Check that the RabbitMQ server is running.'
        d = { ERROR_KEY: msg }
    except ImportError as e:
        d = { ERROR_KEY: str(e)}
    except Exception as e:
        d = { ERROR_KEY: str(e)}
    return d

@login_required
def collage_create(request):
    if request.method == 'GET':
        c = {

            #'collage_form': CollageCreateForm(),
        }
        return render(request, 'collage/create.html', c)




def collage_save(request):
    if request.method == 'POST':
        return HttpResponse('Hello')
    return HttpResponse(status=405)


def delete_upload_async(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_in_executor(None, delete_media_files)
    return redirect('collage:collage-form')


def delete_media_files():
    collages = Collage.objects.all()
    if collages:
        for collage in collages:
            while collage.photos.exists():
                photo = collage.photos.first()
                while photo.cut_photos.exists():
                    photo.cut_photos.first().delete()
                # except ObjectDoesNotExist:
                #     logger.info(f'VIEW:DELETE_UPLOAD_ASYNC: {photo} has no cutphoto')
                photo.delete()
            collage.delete()
    photos = Photo.objects.all()
    for photo in photos:
        photo.delete()
    cut_photos = CutPhoto.objects.all()
    for cut_photo in cut_photos:
        cut_photo.delete()
    logger.info('VIEW: Media files deleted!')
    return 0