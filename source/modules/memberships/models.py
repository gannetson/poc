from django.db import models
from django.utils.translation import ugettext_lazy as _


class Membership(models.Model):
    project = models.ForeignKey('projects.Project', verbose_name=_('project'), related_name='memberships')
    profile = models.ForeignKey('profiles.Profile', verbose_name=_('profile'), related_name='memberships')

    class Meta:
        verbose_name = _('membership')
        verbose_name_plural = _('memberships')

    def __unicode__(self):
        return u"{0} <-> {1}".format(self.project, self.profile)


def create_many_to_many():
    Profile = models.get_model('profiles', 'Profile')
    models.ManyToManyField(
            'projects.Project',
            verbose_name=_('projects'),
            related_name='profiles',
            through=Membership,
            null=True, blank=True
        ).contribute_to_class(Profile, 'projects')
create_many_to_many()
