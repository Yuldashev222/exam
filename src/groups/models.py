from django.db import models
from django.utils.translation import gettext_lazy as _


class ClassGroup(models.Model):
    name = models.CharField(verbose_name=_('Group name'), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
