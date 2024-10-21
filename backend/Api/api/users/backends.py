from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class EmailBackend(BaseBackend):
    """
    Бэкенд для авторизации пользователя по почте
    """
    def authenticate(self, request, username=None, password=None):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
            return user if user.check_password(password) else None
        except (user_model.DoesNotExist, user_model.MultiplyObjectsReturned):
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None

