from django.forms.models import modelform_factory

from tastypie.resources import ALL

from core.api.resources import BaseModelResource
from core.api.validation import CleanedModelFormValidation

from .models import Profile


class ProfileResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = Profile.objects.all()
        resource_name = 'profile'
        filtering = {
            'username': ALL,
        }
        validation = CleanedModelFormValidation(form_class=modelform_factory(Profile))
