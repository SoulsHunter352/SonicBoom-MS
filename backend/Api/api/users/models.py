from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.db import models

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя
    login - уникальные логин пользователя, который используется для входа в систему
    username - никнейм пользователя, который будет виден всем
    email - почта пользователя
    first_name - имя пользователя
    last_name - фамилия пользователя
    role - роль пользователя
    """

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    COMMON = 'common'

    ROLE_CHOICES = (
        (ADMIN, 'ADMIN'),
        (MODERATOR, 'MODERATOR'),
        (COMMON, 'COMMON')
    )

    login = models.CharField(max_length=60, name='login', unique=True, db_index=True)
    username = models.CharField(max_length=50, name='username')
    email = models.EmailField(max_length=60, unique=True, name='email', db_index=True)
    is_active = models.BooleanField(default=True, name='is_active')
    is_staff = models.BooleanField(default=False, name='is_staff')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=COMMON)

    objects = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['username', 'email']
