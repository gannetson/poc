import requests
from requests.exceptions import RequestException
import urlparse
import hashlib
import hmac
import time
import urllib

from django.views.generic.edit import FormView

from .forms import APIForm
from .constants import STATUS_MESSAGES


class ClientView(FormView):

    form_class = APIForm
    template_name = 'client/api_form.html'

    def _do_request(self, form):
        request_method = form.cleaned_data.get('request_method', 'GET').lower()
        post_data = form.cleaned_data.get('post_data')
        request_url = self._build_url(
            request_method=request_method,
            endpoint=form.cleaned_data['endpoint'],
            api_key=form.cleaned_data['api_key'],
            api_secret=form.cleaned_data['api_secret'],
            extra_querystring=form.cleaned_data.get('extra_querystring'),
            post_data=form.cleaned_data.get('post_data'),
        )
        headers = {'content-type': form.cleaned_data['content_type']}
        headers = {'Accept': form.cleaned_data['content_type']}
        handler = getattr(requests, request_method)

        result = handler(request_url, data=post_data, headers=headers)
        return result

    def _build_url(self, request_method, endpoint, api_key, api_secret, extra_querystring=None, post_data=None):
        if not post_data:
            post_data = ''
        parts = urlparse.urlparse(endpoint)

        timestamp = int(time.time())
        data = {
            'api_key': api_key,
            'timestamp': timestamp
        }
        if extra_querystring:
            if extra_querystring.startswith('?'):
                extra_querystring = extra_querystring[1:]
            for key, values in urlparse.parse_qs(extra_querystring).iteritems():
                data[key] = values[0]
        sorted_data = []
        for key in sorted(data.keys()):
            sorted_data.append((key, data[key]))

        message = "{0} {1}?{2}\n\n{3}".format(request_method.upper(), parts.path, urllib.urlencode(sorted_data), post_data)
        digest_maker = hmac.new(str(api_secret), message, hashlib.sha1)
        checksum = digest_maker.hexdigest().lower()

        data.update({'checksum': checksum})

        return u"{0}?{1}".format(
            endpoint,
            urllib.urlencode(data)
        )

    def form_valid(self, form):
        error_message = None
        message = None
        do_html = False
        try:
            response = self._do_request(form)
            message = STATUS_MESSAGES.get(response.status_code, 'Unknown')
            if 'text/html' in response.headers['content-type']:
                do_html = True
        except RequestException, e:
            response = None
            error_message = u"Connection error: {0}".format(e)

        return self.render_to_response(self.get_context_data(
                form=form,
                response=response,
                status_message=message,
                error_message=error_message,
                do_html=do_html,
                content_type=form.cleaned_data['content_type']
        ))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
