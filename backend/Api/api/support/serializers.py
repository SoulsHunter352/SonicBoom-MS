from rest_framework import serializers
from .models import Question, Answer
from users.models import User


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    status = serializers.ChoiceField(choices=Question.STATUSES, default=Question.OPEN)

    class Meta:
        model = Question
        fields = ['id', 'author', 'question_text', 'created_at', 'status']
        
    def create(self, validated_data):
        return Question.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.question_text = validated_data.get('question_text', instance.question_text)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class AnswerSerializer(serializers.ModelSerializer):
    responder = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = ['id', 'responder', 'answer_text', 'question', 'created_at']

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.answer_text = validated_data.get('answer_text', instance.answer_text)
        instance.question = validated_data.get('question', instance.question)
        instance.save()
        return instance
