#coding:utf-8
from django.http import HttpResponseBadRequest

#ajax装饰器
def ajax_required(f):
    def wrap(request,*args,**kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest
        return f(request,*args,**kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__= f.__name__
    return wrap