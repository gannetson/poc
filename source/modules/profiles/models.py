from django.db import models
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    username = models.CharField(_('username'), max_length=255)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profile')

    def __unicode__(self):
        return self.username
