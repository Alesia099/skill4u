from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from .validators import validate_birthday, FullNameValidator
from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
        self,
        email,
        username,
        full_name,
        birthday,
        region,
        city,
        phone,
        password,
        **extra_fields
    ):
        email = self.normalize_email(email)
        full_name = self.model.normalize_username(full_name)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(
            email=email,
            full_name=full_name,
            birthday=birthday,
            region=region,
            city=city,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        full_name,
        birthday,
        region,
        city,
        phone,
        password,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(
            email,
            full_name,
            birthday,
            region,
            city,
            phone,
            password,
            **extra_fields
        )


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