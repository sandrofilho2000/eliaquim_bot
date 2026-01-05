from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Permission
from django.core import validators
from django.utils.translation import gettext_lazy as _
import re
from django.utils import timezone
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError(_('O email precisa ser definido.'))
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not email:
            raise ValueError("Superuser must have an email address.")
        
        if not username:  
            username = email.split("@")[0]

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(
                re.compile(r'^[\w.@+-]+$'),  # Aqui está o ajuste correto
                _('Enter a valid username.'),
                _('invalid')
            )
        ]
    )

    first_name = models.CharField(_('Nome'), max_length=30, blank=True)
    last_name = models.CharField(_('Sobrenome'), max_length=30, blank=True)
    email = models.EmailField(_('Email'), max_length=255, unique=True)
    is_staff = models.BooleanField(_('Membro da equipe'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('Ativo'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('Data de criação'), default=timezone.now)
    email_verified = models.BooleanField(_('Email verificado'), default=False, help_text=_('Indica se o usuário confirmou seu endereço de email.'))
    
    profiles = models.ManyToManyField(
        'profiles.Profile',
        verbose_name=_('Perfis'),
        blank=True,
        related_name='users'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('Permissões do usuário'),
        blank=True,
        related_name="user_permissions", 
        help_text=_('Permissões específicas para este usuário.'),
    )
    
    """ pages_allowed = models.ManyToManyField(
        'pages.page',
        verbose_name=_('Páginas autorizadas'),
        blank=True,
        related_name="user_pages_allowed", 
    )

    subpages_allowed = models.ManyToManyField(
        'pages.subpage',
        verbose_name=_('Subpáginas autorizadas'),
        blank=True,
        related_name="user_subpages_allowed", 
    ) """


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['email']
        indexes = [
            models.Index(fields=['email']),
        ]

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name if full_name else self.email

    def get_short_name(self):
        return self.first_name if self.first_name else self.email
    


    def get_all_custom_permission_codenames(self):
        user_perms = self.user_permissions.all().values_list('content_type__app_label', 'codename')
        profile_perms = Permission.objects.filter(profile_permissions__in=self.profiles.all()).values_list('content_type__app_label', 'codename')
        all_perms = set(user_perms).union(set(profile_perms))
        return {f"{app_label}.{codename}" for app_label, codename in all_perms}