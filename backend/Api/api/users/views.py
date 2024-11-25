from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import login, logout
from .models import User
from .serializers import UserSerializer, LoginSerializer, RegisterUserSerializer, ChangePasswordSerializer


# Create your views here.
class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            object = self.queryset.get(pk=pk)
            return object
        except:
            return None
        # return self.queryset.get(pk=self.kwargs['pk'])

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
        users = self.queryset
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        # создает нового пользователя
        return Response

    def update(self, request, pk=None):
        # изменение данных пользователя(полностью изменяет объект)
        return Response

    def partial_update(self, request, pk=None):
        # изменение данных пользователя(частичное изменение)
        return Response

    def retrieve(self, request, pk=None):
        # возвращает данные об отдельном пользователе
        instance = self.get_object(pk)
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(self.serializer_class(instance).data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        # удаление пользователя
        return Response

    def change_password(self, request):
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
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
