from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import Greeting


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "hello/main_page.html")


def greetings(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "hello/db.html", {"greetings": greetings})


def error_message(request):
    messages.error(request, 'Error message!')
    return index(request)


def success_message(request):
    messages.success(request, 'Success message!')
    return index(request)



