from django.db import models


class Question(models.Model):
    """
    Модель вопроса
    author - связь с автором вопроса
    question_text - текст вопроса
    created_at - дата создания
    status - статус вопроса
    """
    OPEN = 'open'
    CLOSED = 'closed'

    STATUSES = (
        (OPEN, 'OPEN'),
        (CLOSED, 'CLOSED'),
    )
    
    author = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='questions',)
    question_text = models.TextField(verbose_name="Текст вопроса")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=6, choices=STATUSES, default=OPEN)


class Answer(models.Model):
    """
    Модель ответа
    responder - связь с автором ответа
    answer_text - текст ответа
    question - связь с вопросом
    created_at - дата создания
    """
    responder = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='answers', )
    answer_text = models.TextField(verbose_name="Текст ответа")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(auto_now=True, dp_index=True)
