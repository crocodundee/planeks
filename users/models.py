from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

from users.groups import UserGroup
from users.settings import *


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Электронный адресс')
    first_name = models.CharField(max_length=20, blank=True, default='Anonymous', verbose_name='Имя')
    last_name = models.CharField(max_length=20, blank=True, default='User', verbose_name='Фамилия')
    birthday = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    username = None
    user_group = models.ForeignKey(UserGroup,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   default=DEFAULT_GROUP,
                                   verbose_name='Группа')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    full_name.short_description = 'Полное имя'
    full_name = property(full_name)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_default_group(sender, instance=None, created=False, **kwargs):
    if created:
        instance.set_password(raw_password=kwargs.get('password'))
        instance.save()


