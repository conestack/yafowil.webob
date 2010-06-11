import cgi
from UserDict import DictMixin
from webob.request import BaseRequest
from yafowil.base import factory

class WebObRequestAdapter(DictMixin):
    
    def __init__(self, request):
        if isinstance(request, self.__class__):
            # for some rare cases this makes sense             
            request = request.request 
        if not isinstance(request, BaseRequest):
            raise ValueError(\
                'Expecting object based on webob.request.BaseRequest') 
        self.request = request
        self.mixed = request.params.mixed()
        
    def __getitem__(self, key):
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
        return self.request.params.keys()
    
    def __setitem__(self, key, item):
        raise AttributeError('read only, __setitem__ is not supported')
    
    def __delitem__(self, key):
        raise AttributeError('read only, __delitem__ is not supported')
    
def webob_preprocessor(widget, data):
    if not isinstance(data.request, (dict, WebObRequestAdapter)):
        data.request = WebObRequestAdapter(data.request)
    return data

factory.register_global_preprocessors([webob_preprocessor])