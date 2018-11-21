from django.http import HttpResponse
from django.views.decorators.cache import never_cache


from .utils import make_image
import settings

ENC_TYPE, MIME_TYPE = settings.FORMAT


@never_cache
def draw_view(request, code):
    img = make_image(code)
    response = HttpResponse(content_type=MIME_TYPE)
    response['cache-control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    img.save(response, ENC_TYPE)
    return response
