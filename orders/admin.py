from django.contrib import admin
from .models import Order, OrderItem


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']

    list_filter = ['paid', 'created', 'updated']
    #  inline allows you to include a model for appearing on the
    # same edit page as the parent model
    inlines = [OrderItemInline]
# admin.site.register(Order, OrderAdmin)
