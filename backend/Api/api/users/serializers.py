from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  # id пользователя, не может быть изменено
    login = serializers.CharField()  # Уникальный логин пользователя
    email = serializers.EmailField()  # Email пользователя
    username = serializers.CharField()  # Имя пользователя внутри системы
    role = serializers.CharField()  # Роль пользователя

    class Meta:
        model = get_user_model()
        fields = ['id', 'login', 'email', 'username', 'role']  # Список всех полей

    def update(self, instance, validated_data):
        """
        Обновляет данные существующего пользователя.
        :param instance: Экземпляр модели пользователя
        :param validated_data: Проверенные данные из запроса
        :return: Обновленный экземпляр
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  # Устанавливаем новое значение атрибута
        instance.save()  # Сохраняем изменения в базе данных
        return instance


class RegisterUserSerializer(serializers.ModelSerializer):
    login = serializers.CharField(max_length=150)  # Уникальный логин пользователя
    email = serializers.EmailField()  # Email пользователя
    username = serializers.CharField(max_length=150)  # Имя пользователя внутри системы
    password1 = serializers.CharField(write_only=True)  # Пароль пользователя
    password2 = serializers.CharField(write_only=True)  # Повторение пароля пользователя

    class Meta:
        model = User
        fields = ['login', 'email', 'username', 'password1', 'password2']

    def validate(self, data):
        """
        Проверяем совпадение password1 и password2.
        Удаляем поле password2 из данных.
        """
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password2": "Пароли не совпадают."})

        # Удаляем password2, так как оно больше не нужно
        data.pop('password2', None)
        return data

    def create(self, validated_data):
        """
        Создаем нового пользователя с проверенными данными.
        """
        # Извлекаем пароль
        password = validated_data.pop('password1')

        # Создаем пользователя с помощью метода менеджера модели
        user = User.objects.create_user(
            login=validated_data['login'],  # Уникальный логин
            username=validated_data['username'],  # Никнейм пользователя
            email=validated_data['email'],  # Email пользователя
            password=password  # Устанавливаем пароль
        )

        return user


class LoginSerializer(serializers.ModelSerializer):
    login = serializers.CharField(required=True)  # Уникальный логин пользователя
    password = serializers.CharField(write_only=True, required=True)  # Пароль пользователя

    class Meta:
        model = User
        fields = ['login', 'password']

    def validate(self, data):
        """
        Проверяет учетные данные пользователя.
        """
        username = data.get('login')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Неверный логин или пароль.")

        self.context['user'] = user

        return data

    def get_user(self):
        """
        Возвращает аутентифицированного пользователя из контекста.
        """
        return self.context.get('user')


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)  # Старый пароль
    new_password1 = serializers.CharField(write_only=True)  # Новый пароль
    new_password2 = serializers.CharField(write_only=True)  # Повтор нового пароля

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def validate(self, data):
        """
        Проверяет старый пароль и совпадение новых паролей.
        """
        user = self.instance  # Пользователь, чей пароль меняется

        # Проверка старого пароля
        if not check_password(data['old_password'], user.password):
            raise serializers.ValidationError({"old_password": "Старый пароль неверен."})

        # Проверка совпадения новых паролей
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({"new_password2": "Новые пароли не совпадают."})

        # Проверка сложности нового пароля (по стандартным правилам Django)
        validate_password(data['new_password1'], user)

        return data

    def update(self, instance, validated_data):
        """
        Обновляет пароль пользователя.
        """
        new_password = validated_data['new_password1']
        instance.password = make_password(new_password)  # Хэшируем и сохраняем новый пароль
        instance.save()
        return instance