from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import login, logout
from .models import User
from .serializers import UserSerializer, LoginSerializer, RegisterUserSerializer, ChangePasswordSerializer



# Create your views here.
class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterUserSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return self.serializer_class

    def list(self, request):
        """
        Возвращает список всех пользователей.
        """
        users = self.get_queryset()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Создает нового пользователя.
        """
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Пользователь успешно создан", "user": UserSerializer(user).data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Удаляет пользователя.
        """
        try:
            # Получаем пользователя по первичному ключу (pk)
            instance = self.get_queryset().get(pk=pk)
        except User.DoesNotExist:
            # Возвращаем ошибку в формате JSON, если пользователь не найден
            raise NotFound(detail="Пользователь не найден")

        # Удаляем пользователя
        instance.delete()

        # Возвращаем сообщение об успешном удалении
        return Response({"message": "Пользователь успешно удален"}, status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        """
        Частичное обновление данных пользователя.
        """
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        if not instance:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Возвращает данные конкретного пользователя по его ID.
        """
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        if not instance:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        """
        Удаляет пользователя.
        """
        # Получаем пользователя по первичному ключу (pk). Если не найден, выбрасывается исключение Http404.
        instance = get_object_or_404(self.get_queryset(), pk=pk)

        # Удаляем пользователя
        instance.delete()

        # Возвращаем сообщение об успешном удалении
        return Response({"message": "Пользователь успешно удален"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """
        Изменение пароля авторизованного пользователя.
        """
        user = request.user
        serializer = self.get_serializer_class()(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пароль успешно изменен"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Авторизация пользователя с использованием LoginSerializer.
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.get_user()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return Response({"message": "Вы успешно вошли в систему!"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Выход из аккаунта.
    """
    logout(request)
    return Response({"message": "Вы успешно вышли из аккаунта."}, status=status.HTTP_200_OK)
