import cgi
import types
from UserDict import DictMixin
from webob.request import BaseRequest
from yafowil.base import (
    UNSET,
    factory,
)

try:
    from pyramid.interfaces import IRequest
except ImportError:
    IRequest = None

try:
    from pyramid.i18n import get_localizer
except ImportError:
    get_localizer = None


class WebObRequestAdapter(DictMixin):
    
    def __init__(self, request):
        if isinstance(request, self.__class__):
            # for some rare cases this makes sense             
            request = request.request
        # make sure yafowil is testable inside pyramid environment
        pyramid_req = IRequest is not None and IRequest.providedBy(request) 
        if not isinstance(request, BaseRequest) \
          and not pyramid_req \
          and request is not UNSET \
          and request.__class__ is not dict:
            raise ValueError(
                'Expecting object based on webob.request.BaseRequest') 
        self.request = request
        if pyramid_req:
            self.mixed = request.params
        elif request is UNSET:
            self.mixed = dict()
        elif request.__class__ is dict:
            self.mixed = dict()
        else:
            self.mixed = request.params.mixed()
        
    def __getitem__(self, key):
        if hasattr(self.mixed, 'getall'):
            value = self.mixed.getall(key)
            if len(value) < 2:
                value = self.mixed[key]
        else:
            value = self.mixed[key]
        if isinstance(value, cgi.FieldStorage):
            fvalue = dict()
            fvalue['file'] = value.file
            fvalue['filename'] = value.filename
            fvalue['mimetype'] = value.type
            fvalue['headers'] = value.headers
            fvalue['original'] = value
            return fvalue
        return value

    def keys(self):
        if self.request:
            return self.request.params.keys()
        return list()
    
    def __setitem__(self, key, item):
        raise AttributeError('read only, __setitem__ is not supported')
    
    def __delitem__(self, key):
        raise AttributeError('read only, __delitem__ is not supported')


class TranslateCallable(object):
    
    def __init__(self, data):
        if isinstance(data.request, WebObRequestAdapter):
            self.request = data.request.request
        else:
            self.request = data.request
        
    def __call__(self, msg):
        request = self.request
        if request and not isinstance(request, dict) and get_localizer:
            localizer = get_localizer(request)
            return localizer.translate(msg)
        return msg


def webob_preprocessor(widget, data):
    if not isinstance(data.request, (dict, WebObRequestAdapter)):
        data.request = WebObRequestAdapter(data.request)
    if not isinstance(data.translate_callable, TranslateCallable):
        data.translate_callable = TranslateCallable(data)
    return data


def register():
    factory.register_global_preprocessors([webob_preprocessor])