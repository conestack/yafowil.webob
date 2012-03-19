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
    
def webob_preprocessor(widget, data):
    if not isinstance(data.request, (dict, WebObRequestAdapter)):
        data.request = WebObRequestAdapter(data.request)
    return data

def register():
    factory.register_global_preprocessors([webob_preprocessor])