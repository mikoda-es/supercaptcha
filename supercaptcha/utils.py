import random

from PIL import ImageFont, Image, ImageDraw, ImageFilter
from django.core.cache import cache
from django.utils.translation import ugettext_lazy

from supercaptcha import settings


WIDTH = settings.SIZE[0]
HEIGHT = settings.SIZE[1]
SYMBOLS = ugettext_lazy(settings.SYMBOLS)
LENGTH = settings.LENGTH
BG_COLOR = settings.BACKGROUND_COLOR
FG_COLORS = settings.FOREGROUND_COLORS
JUMP = settings.VERTICAL_JUMP
COLORIZE = settings.COLORIZE_SYMBOLS
PREFIX = settings.CACHE_PREFIX


def make_image(code):
    font_name, font_file = random.choice(settings.AVAIL_FONTS)
    cache_name = '{}-{}-size'.format(PREFIX, font_name)
    text = generate_text()
    cache.set('%s-%s' % (PREFIX, code), text, settings.CACHE_TIMEOUT)
    font_size = cache.get(cache_name, 10)
    if fits(text, font_size, font_file):
        while True:
            font_size += 1
            if not fits(text, font_size, font_file):
                font_size -= 1
                break
    else:
        while True:
            font_size -= 1
            if fits(text, font_size, font_file):
                break
    cache.set(cache_name, font_size, settings.CACHE_TIMEOUT)
    font = ImageFont.truetype(font_file, font_size)
    text_size = font.getsize(text)
    icolor = 'RGB'
    if len(BG_COLOR) == 4:
        icolor = 'RGBA'
    img = Image.new(icolor, (WIDTH, HEIGHT), BG_COLOR)
    d = ImageDraw.Draw(img)
    if JUMP:
        if COLORIZE:
            get_color = lambda: random.choice(FG_COLORS)
        else:
            color = random.choice(FG_COLORS)
            get_color = lambda: color
        position = [(WIDTH - text_size[0]) // 2, 0]
        shift_max = HEIGHT - text_size[1]
        shift_min = shift_max // 4
        shift_max = shift_max * 3 // 4
        for char in text:
            l_size = font.getsize(char)
            try:
                position[1] = random.choice(range(shift_min, shift_max + 1))
            except IndexError:
                position[1] = shift_min
            d.text(position, char, font=font, fill=get_color())
            position[0] += l_size[0]
    else:
        position = [(WIDTH - text_size[0]) / 2,
                    (HEIGHT - text_size[1]) / 2]
        d.text(position, text, font=font, fill=random.choice(FG_COLORS))
    for f in settings.FILTER_CHAIN:
        img = img.filter(getattr(ImageFilter, f))
    return img


def fits(text, font_size, font_file):
    font = ImageFont.truetype(font_file, font_size)
    size = font.getsize(text)
    return size[0] < WIDTH and size[1] < HEIGHT


def generate_text():
    return ''.join([random.choice(SYMBOLS) for _ in range(LENGTH)])