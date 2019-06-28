from django.contrib import admin
from .models import Greeting

# Register your models here.


@admin.register(Greeting)
class GreetingAdmin(admin.ModelAdmin):
    list_display = ['when']

