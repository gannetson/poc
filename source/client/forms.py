from django import forms
from django.utils.translation import ugettext_lazy as _


class APIForm(forms.Form):
    endpoint = forms.URLField(label=_('Endpoint'), required=True)
    content_type = forms.ChoiceField(label=_('Content type'), choices=(('application/json', 'JSON'), ('application/xml', 'XML'), ('text/html', 'HTML')))
    request_method = forms.ChoiceField(label=_('Request method'), choices=(('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE'), ('PATCH', 'PATCH'), ('OPTIONS', 'OPTIONS')))
    api_key = forms.CharField(label=_('API Key'), required=True)
    api_secret = forms.CharField(label=_('API secret'), required=True)

    extra_querystring = forms.CharField(label=_('Extra get'), help_text=_('For example: key=value&key2=value'), required=False)
    post_data = forms.CharField(label=_('Post data'), widget=forms.Textarea, required=False)
