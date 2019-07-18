from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    """
    Custom OrderField
    """
    def __init__(self, for_fields=None, *args, **kwargs):
        """

        :param for_fields:  allows us to indicate the fields that the
order has to be calculated with respect to
        :param args:
        :param kwargs:
        """
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)

    #  executed before saving the field into the database
    def pre_save(self, model_instance, add):
        # if a value already exists for this field
        if getattr(model_instance, self.attname) is None:
            # no current value
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with the same field values
                    # for the fields in "for_fields"
                    query = {field: getattr(model_instance, field) \
                             for field in self.for_fields}
                    qs = qs.filter(**query)
                # get the order of the last item
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(OrderField,
                         self).pre_save(model_instance, add)
