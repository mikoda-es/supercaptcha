# -*- coding: utf-8 -*-
from os.path import join, dirname, abspath

from django.conf import settings


SELF_DIR = dirname(abspath(__file__))
FONTS_DIR = join(SELF_DIR, 'fonts')

SYMBOLS = getattr(settings, 'CAPTCHA_SYMBOLS', '123456789ABCDEFGHJKLMNPQRSTVXYZ')
LENGTH = getattr(settings, 'CAPTCHA_LENGTH', 6)

AVAIL_FONTS = getattr(settings, 'CAPTCHA_FONTS', [
        ('vera', join(FONTS_DIR, 'vera.ttf')),
        ('chelseamarketsr', join(FONTS_DIR, 'chelseamarketsr.ttf')),
])

FOREGROUND_COLORS = getattr(settings, 'CAPTCHA_FOREGROUND_COLORS', (
        (0, 0, 0),
        (0x77, 0, 0),
        (0, 0x77, 0),
        (0, 0, 0x77),
        ))

COLORIZE_SYMBOLS = getattr(settings, 'CAPTCHA_COLORIZE_SYMBOLS', True)

BACKGROUND_COLOR = getattr(settings, 'CAPTCHA_BACKGROUND_COLOR', (255, 255, 255))

FILTER_CHAIN = getattr(settings, 'CAPTCHA_FILTER_CHAIN', [])

VERTICAL_JUMP = getattr(settings, 'CAPTCHA_VERTICAL_JUMP', True)

SIZE = getattr(settings, 'CAPTCHA_SIZE', (200, 100))
ALT = getattr(settings, 'CAPTCHA_ALT', 'no robots here')
FORMAT = getattr(settings, 'CAPTCHA_FORMAT', ('JPEG', 'image/jpeg'))

CACHE_PREFIX = getattr(settings, 'CAPTCHA_CACHE_PREFIX', 'captcha')
CACHE_TIMEOUT = getattr(settings, 'CAPTCHA_CACHE_TIMEOUT', 5*60)

DEFAULT_ERROR_MESSAGE = getattr(settings, 'CAPTCHA_DEFAULT_ERROR_MESSAGE', u'The code you entered is wrong.')

REFRESH_LINK_TEXT = getattr(settings, 'CAPTCHA_REFRESH_LINK_TEXT', u'refresh')

REFRESH = getattr(settings, 'CAPTCHA_REFRESH', False)

TEST_MODE = getattr(settings, 'CAPTCHA_TEST_MODE', False)
HOST = getattr(settings, 'CAPTCHA_HOST', '')
