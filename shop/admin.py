from django.contrib import admin
from .models import Category, Product


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

    # value is automatically set using the value of other fields
    prepopulated_fields = {'slug': ('name',)}

# admin.site.register(Category, CategoryAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']

    #  set the fields that can be edited from the list display
    # page of the administration site
    list_editable = ['price', 'stock', 'available']

    prepopulated_fields = {'slug': ('name',)}
