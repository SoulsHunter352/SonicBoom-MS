from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import login, logout
from users.models import User
from users.serializers import UserSerializer, LoginSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        Возвращает список всех пользователей.
        """
        users = self.queryset
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        # создает нового пользователя
        return Response

    def update(self, request, *args, **kwargs):
        # изменение данных пользователя(полностью изменяет объект)
        return Response

    def partial_update(self, request, *args, **kwargs):
        # изменение данных пользователя(частичное изменение)
        return Response

    def retrieve(self, request, *args, **kwargs):
        # возвращает данные об отдельном пользователе
        return Response

    def delete(self, request, *args, **kwargs):
        # удаление пользователя
        return Response

    def change_password(self, request, *args, **kwargs):
        # изменение пароля авторизованного пользователя
        return Response

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Авторизация пользователя с использованием LoginSerializer.
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        # Получаем аутентифицированного пользователя из сериализатора
        user = serializer.get_user()

        # Выполняем вход в систему
        login(request, user)
        return Response({"message": "Вы успешно вошли в систему!"}, status=status.HTTP_200_OK)

    # Возвращаем ошибки сериализатора, если данные невалидны
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Выход из аккаунта.
    """
    logout(request)
    return Response({"message": "Вы успешно вышли из аккаунта."}, status=status.HTTP_200_OK)