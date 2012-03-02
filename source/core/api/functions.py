from django.http import HttpResponse

from tastypie.exceptions import BadRequest
from tastypie.utils import is_valid_jsonp_callback_value
from tastypie.utils.mime import determine_format, build_content_type

from core.api.serializers import HTMLSerializer

from .constants import ERRORS


def error_response(request, error_code=None, message=None, status_code=403, serializer_class=HTMLSerializer, **kwargs):
    context = {}
    if error_code:
        context['error_code'] = error_code

        if not message:
            message = ERRORS[error_code].format(**kwargs)
    if message:
        context['error_message'] = message

    context.update(kwargs)

    serializer = serializer_class()

    desired_format = determine_format(request, serializer)
    options = {}

    if 'text/javascript' in desired_format:
        callback = request.GET.get('callback', 'callback')

        if not is_valid_jsonp_callback_value(callback):
            raise BadRequest('JSONP callback name is invalid.')

        options['callback'] = callback

    serialized = serializer.serialize(context, desired_format, options)
    return HttpResponse(content=serialized, content_type=build_content_type(desired_format), status=status_code)
