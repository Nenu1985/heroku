from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from collage.models import Photo, CutPhoto
from .forms import InputUrlFrom
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404

import threading

from django.views.decorators.csrf import csrf_protect

# from Collag.celery import app



# Create your views here.
def index(request):
    collages = []
    return render(request, 'collage/index.html', {'collages': collages})


def show_image(request, img_id):
    img = get_object_or_404(CutPhoto, id=img_id)

    return render(request, 'collage/image.html', {'photo': img})


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

        photo_instance = Photo.download_photos_by_url(url)
        edited_photo = CutPhoto()
        photo = edited_photo.face_detect(photo_instance)
        context = {
            'form':input_form,
            'photo': photo,
        }
        return redirect(reverse('collage:show_image', kwargs={'img_id': photo.id}))


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


#
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

# def get_celery_worker_status():
#
#     ERROR_KEY = "ERROR"
#     try:
#         insp = app.control.inspect()
#
#         d = insp.stats()
#         if not d:
#             d = { ERROR_KEY: 'No running Celery workers were found.' }
#     except IOError as e:
#         from errno import errorcode
#         msg = "Error connecting to the backend: " + str(e)
#         if len(e.args) > 0 and errorcode.get(e.args[0]) == 'ECONNREFUSED':
#             msg += ' Check that the RabbitMQ server is running.'
#         d = { ERROR_KEY: msg }
#     except ImportError as e:
#         d = { ERROR_KEY: str(e)}
#     except Exception as e:
#         d = { ERROR_KEY: str(e)}
#     return d

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


# @csrf_protect
# def async_example(request):
#
#     if request.is_ajax() and request.method == 'POST':
#         if "count" in request.POST and request.POST["count"]:
#             count = int(request.POST["count"])
#         else:
#             count = 1
#
#
#         processor = Processor()
#
#         thread = threading.Thread(target=processor.process, args=(count,))
#         thread.start()
#
#         return render(request,
#                       "collage/input.html"
#                       )
#
#     else:
#         return render(request,
#                       "collage/input.html"
#                       )



