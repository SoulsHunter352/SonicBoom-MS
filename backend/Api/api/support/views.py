from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer



# class QuestionView(generics.ListAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer


class QuestionView(generics.ListAPIView):
    serializer_class = QuestionSerializer


    def get_queryset(self):
        author_id = self.kwargs.get('author')
        if author_id:
            return Question.objects.filter(author_id=author_id)
        return Question.objects.all()
    

class AnswerView(generics.ListAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def list(self, request):
        answers = self.queryset
        serializer = self.serializer_class(answers, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            answer = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        try:
            answer = Answer.objects.get(pk=pk)
            serializer = self.serializer_class(answer)
            return Response(serializer.data)
        except Answer.DoesNotExist:
            return Response(serializer.errors)

    def update(self, request, pk=None):
        try:
            answer = Answer.objects.get(pk=pk)
            serializer = self.serializer_class(answer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Answer.DoesNotExist:
            return Response(serializer.errors)

    def partial_update(self, request, pk=None):
        try:
            answer = Answer.objects.get(pk=pk)
            serializer = self.serializer_class(answer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Answer.DoesNotExist:
            return Response(serializer.errors)

    def delete(self, request, pk=None):
        try:
            answer = Answer.objects.get(pk=pk)
            answer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Answer.DoesNotExist:
            return Response("Error")