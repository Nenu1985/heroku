from django.http import HttpResponseBadRequest
from functools import wraps

def ajax_required(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    # wrap.__doc__ = f.__doc__
    # wrap.__name__ = f.__name__
    return wrap
