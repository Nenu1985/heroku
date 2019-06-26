from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "hello/main_sidebar.html")


def my_page(request):
    return  render(request, 'hello/mypage.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "hello/db.html", {"greetings": greetings})
