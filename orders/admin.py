from django.contrib import admin
from .models import Order, OrderItem
import csv
import datetime
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    # tell the browser that the response has to be treated as a CSV fle
    response = HttpResponse(content_type='text/csv')
    # Content-Disposition header to indicate that the HTTP response
    # contains an attached fle
    response['Content-Disposition'] = 'attachment; \
        filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    # get the model felds dynamically using the get_fields() method of
    # the model _meta options. We exclude many-to-many and one-to-many
    # relationships
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])

    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


# We customize the display name for the action in the template
# by setting a short_description attribute to the function
export_to_csv.short_description = 'Export to CSV'


# add a link to each Order object in the list display page of the
# administration site
def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('orders:admin-order-detail', args=[obj.id])))


# We have to set the allow_tags attribute of this
# callable to True to avoid auto-escaping
order_detail.allow_tags = True


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('orders:admin-order-pdf', args=[obj.id])))


order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated',
                    order_detail,
                    order_pdf, ]

    list_filter = ['paid', 'created', 'updated']
    #  inline allows you to include a model for appearing on the
    # same edit page as the parent model
    inlines = [OrderItemInline]
    actions = [export_to_csv]
# admin.site.register(Order, OrderAdmin)
