from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.exceptions import ValidationError


class QuestionView(viewsets.ViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def list(self, request):
        filter_params = request.query_params

        for key in filter_params.keys():
            if key not in ['valid_filter1', 'valid_filter2']:
                raise ValidationError(f"Invalid filter: {key}")

        questions = self.queryset.all()
        serializer = self.serializer_class(questions, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data) 
        if serializer.is_valid():
            question = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            questions = Question.objects.get(pk=pk)
            serializer = self.serializer_class(questions)
            return Response(serializer.data)
        except Question.DoesNotExist:
            raise NotFound(detail="Question not found")

    def update(self, request, pk=None):
        try:
            question = Question.objects.get(pk=pk)

            if question.author != request.user and not (request.user.is_admin() or request.user.is_moderator()):
                raise PermissionDenied("You do not have permission to edit this question.")
            
            serializer = self.serializer_class(question, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Question.DoesNotExist:
            raise NotFound(detail="Question not found")

    def partial_update(self, request, pk=None):
        try:
            question = Question.objects.get(pk=pk)

            if question.author != request.user and not (request.user.is_admin() or request.user.is_moderator()):
                raise PermissionDenied("You do not have permission to edit this question.")
            
            serializer = self.serializer_class(question, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Question.DoesNotExist:
            raise NotFound(detail="Question not found")

    def delete(self, request, pk=None):
        try:
            question = Question.objects.get(pk=pk)

            if question.author != request.user and not (request.user.is_admin() or request.user.is_moderator()):
                raise PermissionDenied("You do not have permission to edit this question.")
            
            question.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Question.DoesNotExist:
            raise NotFound(detail="Question not found")
    

class AnswerView(viewsets.ViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def list(self, request):
        filter_params = request.query_params

        for key in filter_params.keys():
            if key not in ['valid_filter1', 'valid_filter2']:
                raise ValidationError(f"Invalid filter: {key}")

        answers = self.queryset.all()
        serializer = self.serializer_class(answers, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            answer = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            answer = Answer.objects.get(pk=pk)
            serializer = self.serializer_class(answer)
            return Response(serializer.data)
        except Answer.DoesNotExist:
            raise NotFound(detail="Answer not found")

    def update(self, request, pk=None):
        try:
            answer = Answer.objects.get(pk=pk)

            if answer.responder != request.user and not (request.user.is_admin() or request.user.is_moderator()):
                raise PermissionDenied("You do not have permission to edit this answer.")
            
            serializer = self.serializer_class(answer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Answer.DoesNotExist:
            raise NotFound(detail="Answer not found")

    def partial_update(self, request, pk=None):
        try:
            answer = Answer.objects.get(pk=pk)

            if answer.responder != request.user and not (request.user.is_admin() or request.user.is_moderator()):
                raise PermissionDenied("You do not have permission to edit this answer.")
            
            serializer = self.serializer_class(answer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Answer.DoesNotExist:
            raise NotFound(detail="Answer not found")

    def delete(self, request, pk=None):
        try:
            answer = Answer.objects.get(pk=pk)

            if answer.responder != request.user and not (request.user.is_admin() or request.user.is_moderator()):
                raise PermissionDenied("You do not have permission to edit this answer.")
            
            answer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Answer.DoesNotExist:
            raise NotFound(detail="Answer not found")