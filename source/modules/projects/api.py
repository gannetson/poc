from django.forms.models import modelform_factory

from tastypie.resources import ALL

from core.api.resources import BaseModelResource
from core.api.validation import CleanedModelFormValidation

from .models import Project


class ProjectResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = Project.objects.all()
        resource_name = 'project'
        filtering = {
            'name': ALL,
            'slug': ALL,
        }
        validation = CleanedModelFormValidation(form_class=modelform_factory(Project))
