from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'genre', AnswerView)
router.register(r'song', QuestionView)
urlpatterns = []
urlpatterns += router.urls