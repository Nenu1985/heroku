from django.contrib import admin
from .models import Collage, Photo, CutPhoto


# Register your models here.
# class PhotoSizeInline(admin.TabularInline): # табулированно-табличная форма
# #class ChoiceInline(admin.StackedInline):  # списочно-стековая форма
#     model = PhotoSize



#class CollageAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text']

    # fieldsets = [
    #         ('Photo Number', {'fields': ['photo_number']}),
    #         ('Cols number', {'fields': ['cols_number']}),
    #         ('Date information', {'fields': ['create_date'], 'classes': ['collapse']}),
    #     ]
    #inlines = [PhotoSize]
    # list_display = ('photo_number', 'create_date', 'was_published_recently')
    # list_filter = ['create_date']

#
# @admin.register(Collage)
# class CollageAdmin(admin.ModelAdmin):
#     fields = [
#         #'create_date',
#
#     ]

@admin.register(Collage)
class CollageAdmin(admin.ModelAdmin):
    list_display = ('id','cols_number', 'photo_tag', 'create_date',
                    'photo_size', 'final_img',)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo_url', 'img_location', 'date',)
    date_hierarchy = 'date'


@admin.register(CutPhoto)
class CutPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'img_location', 'date', 'photo_type')
    date_hierarchy = 'date'
