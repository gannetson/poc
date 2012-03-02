import hashlib
import hmac
import logging
import time
import urllib

from django.conf import settings
from django.utils.crypto import constant_time_compare

from tastypie.authentication import Authentication

from .functions import error_response
from .models import Client

logger = logging.getLogger('api.authentication')


class LazyClient(object):
    api_key = None

    def __init__(self, api_key):
        self.api_key = api_key

    def __get__(self, request, obj_type=None):
        if self.api_key is None:
            return None

        if not hasattr(request, '_cached_client'):
            try:
                request._cached_client = Client.objects.get(api_key=self.api_key)
                logger.debug('Found client: {0}'.format(request._cached_client))
            except Client.DoesNotExist:
                request._cached_client = None
        return request._cached_client


class ChecksumAuthentication(Authentication):

    def _get_client(self, request, api_key):
        """Try to get the client based on the identifier

        **Args:**
        * *api_key:* The unique client api key

        *Returns:* A Client object or None

        """
        request.__class__.api_client = LazyClient(api_key)
        return request.api_client

    def _valid_timestamp(self, request, timestamp):
        """Valdates the given timestamp against our UTC timestamp including a small grace period

        **Args:**
        * *timestamp:* The timestamp passed to us

        *Returns:* None
        *Raises:* `ErrorResponse`
        """
        try:
            now = int(time.time())
            timestamp = int(timestamp)
            delta = settings.API_TIMESTAMP_TIMEOUT
            skew = max(timestamp - now, now - timestamp)
            if skew < delta:
                # Valid, return
                return True
            logger.debug('Timestamp no longer valid: {0} +- {1} != {2}'.format(timestamp, settings.API_TIMESTAMP_TIMEOUT, now))
            return error_response(request, error_code='0003', received_timestamp=timestamp, our_timestamp=now)
        except TypeError:
            pass
        logger.debug('Timestamp invalid: `{0}`'.format(timestamp))
        return error_response(request, error_code='0002', received_timestamp=timestamp)

    def _get_params(self, request):
        """Build the params dict object based on the request
        Note: It will still contain the checksum param!

        **Args:**
        * *request:* The request

        *Returns:* A querydict with all the relevant params

        """
        params = request.GET.copy()
        return params

    def _get_message(self, request, params, path):
        """Build the message to encode using the params

        **Args:**
        * *request:* The request
        * *params:* A dict-like object with request parameters
        * *path:* The request path

        *Returns:* a unicode string
        """
        sorted_params = []
        for key in sorted(params.keys()):
            sorted_params.append((key.lower(), params[key]))
        return u"{0} {1}?{2}\n\n{3}".format(request.method, path, urllib.urlencode(sorted_params), request.raw_post_data)

    def is_authenticated(self, request, **kwargs):
        """
        Identifies if the user is authenticated to continue or not.

        Should return either ``True`` if allowed, ``False`` if not or an
        ``HttpResponse`` if you need something custom.
        """
        params = self._get_params(request)

        checksum = params.get('checksum', '').lower()
        if checksum:
            del params['checksum']

        # Get the client
        api_key = params.get('api_key')
        client = self._get_client(request, api_key)
        if client is None:
            # Return none so the permissions get an anonymous user
            return error_response(request, message='No (valid) api_key specified', status_code=401)

        # Make sure timestamp is valid
        timestamp = params.get('timestamp')
        result = self._valid_timestamp(request, timestamp)
        if result != True:
            return result

        # Build our own checksum
        # We need to cast to string, hmac can't handle unicode
        secret = str(client.secret)
        message = self._get_message(request, params, request.path)
        digest_maker = hmac.new(secret, message, hashlib.sha1)
        our_checksum = digest_maker.hexdigest().lower()

        # Compare, we use constant time here for extra security
        if not constant_time_compare(unicode(our_checksum), unicode(checksum)):
            logger.debug('Checksum invalid; expected: {0}, got: {1}, message_string: {2}'.format(our_checksum, checksum, message))
            return error_response(request, error_code='0001')

        return True

    def get_identifier(self, request):
        """
        Provides a unique string identifier for the requestor.

        This implementation returns the client api key or a combination of IP address and hostname.
        """
        client = self._get_client(request, request.GET.get('api_key'))
        if client:
            return client.api_key
        return "%s_%s" % (request.META.get('REMOTE_ADDR', 'noaddr'), request.META.get('REMOTE_HOST', 'nohost'))
