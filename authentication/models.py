# models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, phone, password=password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('captain', 'captain'),
        ('customer', 'customer'),
    )
    RIDE_CHOICES = (
        ('RideAc', 'RideAc'),
        ('Echo', 'Echo'),
    )

    username = None
    username_validator = None

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, unique=True)
    country_code = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,blank=True)
    ride_category = models.CharField(max_length=20, choices=RIDE_CHOICES,blank=True)

    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_sso = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='customuser_set', related_query_name='user')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='customuser_set', related_query_name='user')

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.name
