from django.forms.models import modelform_factory

from tastypie import fields
from tastypie.resources import ALL_WITH_RELATIONS

from core.api.resources import BaseModelResource
from core.api.validation import CleanedModelFormValidation

from modules.profiles.api import ProfileResource
from modules.projects.api import ProjectResource

from .models import Membership


class MembershipResource(BaseModelResource):
    project = fields.ToOneField(ProjectResource, 'project')
    profile = fields.ToOneField(ProfileResource, 'profile')

    class Meta(BaseModelResource.Meta):
        queryset = Membership.objects.all()
        resource_name = 'membership'
        filtering = {
            'project': ALL_WITH_RELATIONS,
            'profile': ALL_WITH_RELATIONS,
        }
        validation = CleanedModelFormValidation(form_class=modelform_factory(Membership))

# TODO: Monkeypatch project/profile to "know" about memberships?
