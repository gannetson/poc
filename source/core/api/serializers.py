from django.core.serializers import json
from django.template.loader import render_to_string
from django.utils import simplejson

from tastypie.serializers import Serializer


class HTMLSerializer(Serializer):
    """Allows for html output in user readable json"""

    def to_pretty_json(self, data, options=None):
        """
        Given some Python data, produces JSON output.
        """
        options = options or {}
        data = self.to_simple(data, options)
        return simplejson.dumps(data, cls=json.DjangoJSONEncoder, sort_keys=True, indent=4)

    def to_html(self, *args, **kwargs):
        json = self.to_pretty_json(*args, **kwargs)
        return render_to_string('api/api.html', {'json': json})
