from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from .validators import validate_birthday, FullNameValidator
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    full_name_validator = FullNameValidator

    email = models.EmailField(_('email'), unique=True)
    full_name = models.CharField(_('full_name'), max_length=100, blank=True, unique=True)
    #birthday = models.DateField(_("birthday"), validators=[validate_birthday], blank=True)
    region = models.CharField(_("region"), max_length=50)
    city = models.CharField(_("city"), max_length=50)
    phone = PhoneNumberField(_("phone"))
    place_of_study = models.CharField(_("place of study"), max_length=50)
    place_of_work = models.CharField(_("place of work"), max_length=50)
    education = models.CharField(_("education"), max_length=50)
    motivation = models.TextField(blank=True, verbose_name=_("about"))
    is_active = models.BooleanField(default=True, verbose_name=_("active"))
    is_staff = models.BooleanField(default=False, verbose_name=_("staff"))
    is_teacher = models.BooleanField(default=False, verbose_name=_("teacher"))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_("date joined"))
    avatar = models.ImageField(upload_to='avatars/', default='none/blank.jpg', height_field=None, width_field=None)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Отправляет электронное письмо этому пользователю.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)