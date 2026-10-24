from node.utils import UNSET
from types import SimpleNamespace
from unittest import mock
from webob import Request
from webob.multidict import MultiDict
from yafowil import webob as yafowil_webob
from yafowil.base import factory
from yafowil.base import RuntimeData
from yafowil.tests import YafowilTestCase
from yafowil.webob import register
from yafowil.webob import TranslateCallable
from yafowil.webob import webob_preprocessor
from yafowil.webob import WebObRequestAdapter
import cgi
import importlib
import sys


def pyramid_request(*params):
    return SimpleNamespace(params=MultiDict(params))


def pyramid_request_interface():
    iface = mock.Mock()
    iface.providedBy.return_value = True
    return iface


class TestWebObRequestAdapter(YafowilTestCase):
    def test_params_are_mixed(self):
        request = Request.blank('/?a=1&b=2&b=3')
        adapter = WebObRequestAdapter(request)
        self.assertIs(adapter.request, request)
        self.assertEqual(adapter['a'], '1')
        self.assertEqual(adapter['b'], ['2', '3'])
        with self.assertRaises(KeyError):
            adapter['c']

    def test_keys_iter_len(self):
        adapter = WebObRequestAdapter(Request.blank('/?a=1&b=2&b=3'))
        self.assertEqual(list(adapter.keys()), ['a', 'b', 'b'])
        self.assertEqual(list(adapter), ['a', 'b', 'b'])
        self.assertEqual(len(adapter), 3)

    def test_wraps_adapter(self):
        request = Request.blank('/?a=1')
        adapter = WebObRequestAdapter(WebObRequestAdapter(request))
        self.assertIs(adapter.request, request)
        self.assertEqual(adapter['a'], '1')

    def test_unset_request(self):
        adapter = WebObRequestAdapter(UNSET)
        self.assertEqual(adapter.mixed, {})
        self.assertEqual(list(adapter.keys()), [])
        self.assertEqual(list(adapter), [])
        self.assertEqual(len(adapter), 0)

    def test_dict_request(self):
        adapter = WebObRequestAdapter({'a': '1'})
        self.assertEqual(adapter.mixed, {})

    def test_invalid_request(self):
        with self.assertRaises(ValueError) as arc:
            WebObRequestAdapter(object())
        self.assertEqual(
            str(arc.exception), 'Expecting object based on webob.request.BaseRequest'
        )

    def test_file_upload(self):
        request = Request.blank('/', POST={'upload': ('foo.txt', b'content')})
        value = WebObRequestAdapter(request)['upload']
        self.assertEqual(
            sorted(value), ['file', 'filename', 'headers', 'mimetype', 'original']
        )
        self.assertEqual(value['file'].read(), b'content')
        self.assertEqual(value['filename'], 'foo.txt')
        self.assertEqual(value['mimetype'], 'text/plain')
        self.assertEqual(
            value['headers']['Content-Disposition'],
            'form-data; name="upload"; filename="foo.txt"',
        )
        self.assertIsInstance(value['original'], cgi.FieldStorage)

    def test_read_only(self):
        adapter = WebObRequestAdapter(Request.blank('/?a=1'))
        with self.assertRaises(AttributeError) as arc:
            adapter['a'] = '2'
        self.assertEqual(str(arc.exception), 'read only, __setitem__ is not supported')
        with self.assertRaises(AttributeError) as arc:
            del adapter['a']
        self.assertEqual(str(arc.exception), 'read only, __delitem__ is not supported')

    def test_pyramid_request(self):
        request = pyramid_request(('a', '1'), ('b', '2'), ('b', '3'))
        with mock.patch.object(yafowil_webob, 'IRequest', pyramid_request_interface()):
            adapter = WebObRequestAdapter(request)
        self.assertIs(adapter.mixed, request.params)
        self.assertEqual(adapter['a'], '1')
        self.assertEqual(adapter['b'], ['2', '3'])


class TestTranslateCallable(YafowilTestCase):
    def test_unwraps_adapter(self):
        request = Request.blank('/')
        data = SimpleNamespace(request=WebObRequestAdapter(request))
        self.assertIs(TranslateCallable(data).request, request)

    def test_dict_request_returns_message(self):
        translate = TranslateCallable(SimpleNamespace(request={}))
        self.assertEqual(translate('msg'), 'msg')

    def test_without_localizer_returns_message(self):
        data = SimpleNamespace(request=Request.blank('/'))
        with mock.patch.object(yafowil_webob, 'get_localizer', None):
            self.assertEqual(TranslateCallable(data)('msg'), 'msg')

    def test_translates_with_localizer(self):
        request = Request.blank('/')
        localizer = mock.Mock()
        localizer.translate.return_value = 'translated'
        get_localizer = mock.Mock(return_value=localizer)
        data = SimpleNamespace(request=request)
        with mock.patch.object(yafowil_webob, 'get_localizer', get_localizer):
            self.assertEqual(TranslateCallable(data)('msg'), 'translated')
        get_localizer.assert_called_once_with(request)
        localizer.translate.assert_called_once_with('msg')


class TestPreprocessor(YafowilTestCase):
    def test_webob_preprocessor(self):
        data = RuntimeData(request=Request.blank('/?a=1'))
        webob_preprocessor(None, data)
        adapter = data.request
        translate = data.translate_callable
        self.assertIsInstance(adapter, WebObRequestAdapter)
        self.assertIsInstance(translate, TranslateCallable)
        webob_preprocessor(None, data)
        self.assertIs(data.request, adapter)
        self.assertIs(data.translate_callable, translate)

    def test_webob_preprocessor_keeps_dict_request(self):
        data = RuntimeData(request={'a': '1'})
        webob_preprocessor(None, data)
        self.assertEqual(data.request, {'a': '1'})

    def test_extract_webob_request(self):
        factory.register_global_preprocessors([webob_preprocessor])
        widget = factory('text', name='field')
        data = widget.extract(Request.blank('/?field=value'))
        self.assertEqual(data.extracted, 'value')

    def test_register(self):
        with mock.patch.object(factory, 'register_global_preprocessors') as reg:
            register()
        reg.assert_called_once_with([webob_preprocessor])


class TestWithoutPyramid(YafowilTestCase):
    def test_pyramid_imports_are_optional(self):
        try:
            with mock.patch.dict(
                sys.modules, {'pyramid.interfaces': None, 'pyramid.i18n': None}
            ):
                importlib.reload(yafowil_webob)
                self.assertIsNone(yafowil_webob.IRequest)
                self.assertIsNone(yafowil_webob.get_localizer)
        finally:
            importlib.reload(yafowil_webob)
