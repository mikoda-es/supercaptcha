import os
from random import random
from threading import local

from django import forms
from django.core.cache import cache
from django.urls import reverse
from django.forms.utils import flatatt
from django.utils.translation import ugettext_lazy

from supercaptcha import settings as conf
from .utils import generate_text
from .views import draw_view

_thread_locals = local()


REFRESH = conf.REFRESH
CODE_ATTR_NAME = '_captcha_code'
WIDTH = conf.SIZE[0]
HEIGHT = conf.SIZE[1]
LENGTH = conf.LENGTH
REFRESH_LINK_TEXT = ugettext_lazy(conf.REFRESH_LINK_TEXT)
PREFIX = conf.CACHE_PREFIX
ERROR_MESSAGE = conf.DEFAULT_ERROR_MESSAGE


def get_current_code():
    if not hasattr(_thread_locals, CODE_ATTR_NAME):
        code = os.urandom(16).hex()
        setattr(_thread_locals, CODE_ATTR_NAME, code)
    return getattr(_thread_locals, CODE_ATTR_NAME)


def set_current_code(value):
    setattr(_thread_locals, CODE_ATTR_NAME, value)


def empty_current_code():
    if hasattr(_thread_locals, CODE_ATTR_NAME):
        delattr(_thread_locals, CODE_ATTR_NAME)


class CaptchaImageWidget(forms.Widget):

    @property
    def template_name(self):
        return 'supercaptcha/widgets/captcha_with_refresh.html' if REFRESH else 'supercaptcha/widgets/captcha.html'

    def get_context(self, name, value, attrs, *a, **kwargs):
        context = super().get_context(name, value, attrs)
        code = get_current_code()
        empty_current_code()
        src = reverse(draw_view, kwargs={'code': code})
        input_attrs = self.build_attrs(attrs, extra_attrs={'type': 'text', 'name': name})
        context['widget'].update({
            'src': src,
            'host': conf.HOST,
            'input_attrs': flatatt(input_attrs),
            'alt': conf.ALT,
            'width': WIDTH,
            'length': LENGTH,
            'height': HEIGHT,
            'rnd': random(),
            'refresh_text': REFRESH_LINK_TEXT

        })
        return context


class HiddenCodeWidget(forms.HiddenInput):

    def get_context(self, name, value, attrs):
        if value is None:
            empty_current_code()
        if not value:
            value = get_current_code()
        else:
            set_current_code(value)
        return super().get_context(name, value, attrs)


class CaptchaWidget(forms.MultiWidget):

    def __init__(self, attrs=None, code=None):
        attrs = attrs or {}
        widgets = (HiddenCodeWidget(attrs=attrs), CaptchaImageWidget(attrs=attrs))
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split()
        return [None, None]

    @classmethod
    def id_for_label(cls, id_):
        if id_:
            id_ += '_1'
        return id_


class CaptchaField(forms.MultiValueField):
    widget = CaptchaWidget

    default_error_messages = {
        'wrong': ugettext_lazy(ERROR_MESSAGE),
        'required': ugettext_lazy(u'This field is required.'),
        'internal': ugettext_lazy(u'Internal error.'),
    }

    def __init__(self, *args, **kwargs):
        fields = (
            forms.CharField(max_length=32, min_length=32),
            forms.CharField(max_length=conf.LENGTH, min_length=conf.LENGTH),
        )
        super(CaptchaField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        return ' '.join(data_list)

    def clean(self, value):
        if len(value) != 2:
            raise forms.ValidationError(self.error_messages['wrong'])
        code, text = value
        if not text:
            raise forms.ValidationError(self.error_messages['required'])
        if conf.TEST_MODE and text.lower() == 'passed':
            # automatically pass the test
            return True
        cached_text = cache.get('%s-%s' % (PREFIX, code))
        cache.set('%s-%s' % (PREFIX, code), generate_text(), conf.CACHE_TIMEOUT)
        if not cached_text:
            raise forms.ValidationError(self.error_messages['internal'])
        if text.lower() != cached_text.lower():
            raise forms.ValidationError(self.error_messages['wrong'])
