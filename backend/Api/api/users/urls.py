from django.urls import path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('login/', views.login_view, name='login'),
]

urlpatterns += router.urls
