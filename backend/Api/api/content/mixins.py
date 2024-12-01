from rest_framework.permissions import AllowAny, IsAuthenticated


class CustomPermissionMixin:
    def get_permissions(self):
        if self.action == 'retrieve':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]
