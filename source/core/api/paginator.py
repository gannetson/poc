import urllib
from tastypie.paginator import Paginator as BasePaginator

class Paginator(BasePaginator):

    _skip_params = ('api_key', 'timestamp', 'checksum')

    def _generate_uri(self, limit, offset):
        if self.resource_uri is None:
            return None

        request_params = dict([k, v.encode('utf-8')] for k, v in self.request_data.items() if k not in self._skip_params)
        request_params.update({'limit': limit, 'offset': offset})
        return '%s?%s' % (
            self.resource_uri,
           urllib.urlencode(request_params)
        )
