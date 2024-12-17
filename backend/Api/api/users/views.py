from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import  permission_classes, action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import  logout
from .models import User
from .serializers import UserSerializer, LoginSerializer, RegisterUserSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.decorators import api_view
from rest_framework.response import Response





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
def login(request):
    """
    Авторизация пользователя с использованием LoginSerializer и сохранением refresh-токена в куки.
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.get_user()

        # Генерация токенов
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Установка refresh-токена в HttpOnly cookie
        response = Response({
            "message": "Вы успешно вошли в систему!",
            "access_token": str(access_token),
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,  # Нельзя прочитать через JavaScript
            secure=True,  # Только по HTTPS
            samesite='Strict',  # Защита от CSRF
            max_age=7 * 24 * 60 * 60  # 7 дней
        )

        return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def check_auth(request):
    """
    Проверка авторизации пользователя через refresh-токен из куки.
    """
    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
        return Response({"authenticated": False, "message": "Токен отсутствует"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Проверяем refresh-токен
        refresh = RefreshToken(refresh_token)
        user = refresh.access_token.payload['user_id']  # Или используйте библиотеку для извлечения юзера

        return Response({
            "authenticated": True,
            "message": "Пользователь авторизован",
        }, status=status.HTTP_200_OK)

    except TokenError:
        return Response({"authenticated": False, "message": "Токен недействителен"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Выход из аккаунта.
    """
    logout(request)
    return Response({"message": "Вы успешно вышли из аккаунта."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def refresh_access_token(request):
    # Извлекаем refresh токен из cookie
    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
        return Response({"error": "Refresh token missing"}, status=400)

    try:
        # Проверка refresh токена
        refresh = RefreshToken(refresh_token)
        # Генерация нового access токена
        new_access_token = refresh.access_token

        # Возвращаем новый access токен в ответе
        return Response({
            'access_token': str(new_access_token),
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)
