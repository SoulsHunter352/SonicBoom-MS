from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, login, password, username, email, **other_fields):
        """
        Функция для создания пользователя
        """
        if not login:
            raise ValueError('login должен быть не пустой')
        email = self.normalize_email(email)
        user = get_user_model().objects.create(login=login, username=username, email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, login, password, username, email, **other_fields):
        """ 
        Функция создания обычного пользователя
        """
        other_fields.setdefault('is_superuser', False)
        return self._create_user(login, password, username, email, **other_fields)

    def create_superuser(self, login, password, username, email, **other_fields):
        """
        Функция создания суперпользователя
        """
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        if not other_fields.get('is_superuser'):
            raise ValueError('У суперпользователя должен быть параметр is_superuser=True')
        return self._create_user(login, password, username, email, **other_fields)
