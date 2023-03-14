from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from groups.models import ClassGroup


class CustomUser(AbstractUser):
    username = None
    group = models.ForeignKey(ClassGroup, on_delete=models.SET_NULL, null=True)  # or CASCADE
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('is student'), default=False)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    phone_number = models.CharField(
        max_length=13, blank=True,
        validators=[RegexValidator(regex=r'^+998\d{9}', message='e.g: "+998912345678"')]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('student')
        verbose_name_plural = _('students')
