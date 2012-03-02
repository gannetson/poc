from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .utils import KeyGenerator


class Client(models.Model):
    description = models.CharField(
        verbose_name=_('short description'),
        max_length=255
    )
    api_key = models.SlugField(
        verbose_name=_('API key'),
        validators=[MinLengthValidator(32)],
        max_length=32,
        unique=True,
        db_index=True,
        default=KeyGenerator(32)
    )
    secret = models.CharField(
        verbose_name=_('secret key'),
        validators=[MinLengthValidator(8)],
        max_length=100,
        default=KeyGenerator(50)
    )
    resources = models.ManyToManyField('api.Resource', verbose_name=_('resources'), related_name='clients')

    class Meta:
        verbose_name = _('client')
        verbose_name_plural = _('clients')

    def __unicode__(self):
        return u"{0} ({1})".format(self.description, self.api_key)


class Resource(models.Model):
    resource_identifier = models.SlugField(_('resource identifier'), unique=True)

    class Meta:
        verbose_name = _('API resource')
        verbose_name_plural = _('API resources')

    def __unicode__(self):
        return self.resource_identifier
