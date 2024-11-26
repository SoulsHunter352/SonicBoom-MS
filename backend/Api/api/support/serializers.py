from rest_framework import serializers
from .models import Question, Answer
from users.models import User


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('author', 'question_text', 'created_at', 'status')


class AnswerSerializer(serializers.ModelSerializer):
    responder = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = ['responder', 'answer_text', 'question', 'created_at']

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.responder = validated_data.get('responder', instance.responder)
        instance.answer_text = validated_data.get('answer_text', instance.answer_text)
        instance.question = validated_data.get('question', instance.question)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance
