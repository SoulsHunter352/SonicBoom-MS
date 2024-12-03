from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'answers', AnswerView)
router.register(r'questions', QuestionView)
urlpatterns = []
urlpatterns += router.urls