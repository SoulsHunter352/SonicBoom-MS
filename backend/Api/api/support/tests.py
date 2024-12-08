from django.test import TestCase
from support.models import Question, Answer
from users.models import User
from support.serializers import QuestionSerializer, AnswerSerializer
from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework import status


class QuestionSerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@example.com", password="password")

    def test_create_question_positive(self):
        """Тест Б101: Позитивный тест на создание вопроса"""
        data = {'author': self.user.id, 'question_text': 'Как поменять пароль?', 'status': 'open'}
        serializer = QuestionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        question = serializer.save()
        self.assertEqual(question.author, self.user)
        self.assertEqual(question.question_text, 'Как поменять пароль?')
        self.assertEqual(question.status, 'open')

    def test_create_question_negative(self):
        """Тест Б102: Негативный тест на создание вопроса"""
        data = {'author': None, 'question_text': '', 'status': 'open'}
        serializer = QuestionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('author', serializer.errors)
        self.assertIn('question_text', serializer.errors)

    def test_update_question_positive(self):
        """Тест Б103: Позитивный тест на обновление вопроса"""
        question = Question.objects.create(author=self.user, question_text='Прошлый вопрос', status='open')
        data = {'question_text': 'Как поменять пароль?', 'status': 'closed'}
        serializer = QuestionSerializer(instance=question, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_question = serializer.save()
        self.assertEqual(updated_question.question_text, 'Как поменять пароль?')
        self.assertEqual(updated_question.status, 'closed')

    def test_update_question_negative(self):
        """Тест Б104: Негативный тест на обновление вопроса"""
        question = Question.objects.create(author=self.user, question_text='Прошлый вопрос', status='open')
        data = {'question_text': '', 'status': 'closed'}
        serializer = QuestionSerializer(instance=question, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn('question_text', serializer.errors)


class AnswerSerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="responder", email="responder@example.com", password="password")
        self.question = Question.objects.create(author=self.user, question_text='Как поменять пароль?', status='open')

    def test_create_answer_positive(self):
        """Тест Б105: Позитивный тест на создание ответа"""
        data = {'responder': self.user.id, 'answer_text': 'На вкладке "Сменить пароль" в личном кабинете.', 'question': self.question.id}
        serializer = AnswerSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        answer = serializer.save()
        self.assertEqual(answer.responder, self.user)
        self.assertEqual(answer.answer_text, 'На вкладке "Сменить пароль" в личном кабинете.')
        self.assertEqual(answer.question, self.question)

    def test_create_answer_negative(self):
        """Тест Б106: Негативный тест на создание ответа"""
        data = {'responder': None, 'answer_text': '', 'question': self.question.id}
        serializer = AnswerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('responder', serializer.errors)
        self.assertIn('answer_text', serializer.errors)

    def test_update_answer_positive(self):
        """Тест Б107: Позитивный тест на обновление ответа"""
        answer = Answer.objects.create(responder=self.user, answer_text='Прошлый ответ', question=self.question)
        data = {'answer_text': 'Новый ответ'}
        serializer = AnswerSerializer(instance=answer, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_answer = serializer.save()
        self.assertEqual(updated_answer.answer_text, 'Новый ответ')

    def test_update_answer_negative(self):
        """Тест Б108: Негативный тест на обновление ответа"""
        answer = Answer.objects.create(responder=self.user, answer_text='Прошлый ответ', question=self.question)
        data = {'answer_text': ''}
        serializer = AnswerSerializer(instance=answer, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn('answer_text', serializer.errors)


class QuestionViewSetTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="password", login='login')
        self.client.force_authenticate(user=self.user)
        self.question = Question.objects.create(
            author=self.user,
            question_text="Как поменять пароль?",
            status=Question.OPEN
        )

    def test_B109_list_all_questions(self):
        """Тест Б109: Положительный, метод list, запрос без фильтров"""
        response = self.client.get('/api/questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_B110_list_invalid_filters(self):
        """Тест Б110: Отрицательный, метод list, запрос с неправильными параметрами"""
        response = self.client.get('/api/questions/?nonexistent_filter=true')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_B111_create_question(self):
        """Тест Б111: Положительный, метод create"""
        data = {'author': self.user.id, 'question_text': 'Как добавить трек?'}
        response = self.client.post('/api/questions/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['question_text'], 'Как добавить трек?')

    def test_B112_create_invalid_question(self):
        """Тест Б112: Отрицательный, метод create"""
        data = {'author': self.user.id, 'question_text': ''}
        response = self.client.post('/api/questions/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_B113_retrieve_question(self):
        """Тест Б113: Положительный, метод retrieve"""
        response = self.client.get(f'/api/questions/{self.question.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.question.id)

    def test_B114_retrieve_nonexistent_question(self):
        """Тест Б114: Отрицательный, метод retrieve"""
        response = self.client.get('/api/questions/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_B115_update_question(self):
        """Тест Б115: Положительный, метод update"""
        data = {'author': self.user.id, 'question_text': 'Обновленный текст'}
        response = self.client.put(f'/api/questions/{self.question.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question_text'], 'Обновленный текст')

    def test_B116_update_invalid_question(self):
        """Тест Б116: Отрицательный, метод update"""
        data = {'author': self.user.id, 'question_text': ''}
        response = self.client.put(f'/api/questions/{self.question.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_B117_partial_update_question(self):
        """Тест Б117: Положительный, метод partial_update"""
        data = {'question_text': 'Частичное обновление текста'}
        response = self.client.patch(f'/api/questions/{self.question.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question_text'], 'Частичное обновление текста')

    def test_B118_partial_update_invalid_question(self):
        """Тест Б118: Отрицательный, метод partial_update"""
        data = {'question_text': ''}
        response = self.client.patch(f'/api/questions/{self.question.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_B119_delete_question(self):
        """Тест Б119: Положительный, метод delete"""
        response = self.client.delete(f'/api/questions/{self.question.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Question.objects.filter(id=self.question.id).exists())

    def test_B120_delete_nonexistent_question(self):
        """Тест Б120: Отрицательный, метод delete"""
        response = self.client.delete('/api/questions/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AnswerViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="password", login='login')
        self.client.force_authenticate(user=self.user)
        self.user1 = User.objects.create_user(username="testuser1", email="testuser1@example.com", password="password1", login='login1')
        self.client.force_authenticate(user=self.user1)
        self.question = Question.objects.create(
            author=self.user,
            question_text="Как поменять пароль?",
            status=Question.OPEN
        )
        self.answer = Answer.objects.create(
            answer_text="На вкладке 'Сменить пароль' в личном кабинете.",
            question=self.question,
            responder=self.user1
        )

    def test_B121_list_all_answers(self):
        """Тест Б121: Положительный, метод list, запрос без фильтров"""
        response = self.client.get('/api/answers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_B122_list_invalid_filters(self):
        """Тест Б122: Отрицательный, метод list, запрос с неправильными параметрами"""
        response = self.client.get('/api/answers/?nonexistent_filter=true')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_B123_create_answer(self):
        """Тест Б123: Положительный, метод create"""
        data = {'responder': self.user1.id, 'answer_text': 'Ответ на вопрос.', 'question': self.question.id,}
        response = self.client.post('/api/answers/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['answer_text'], 'Ответ на вопрос.')

    def test_B124_create_invalid_answer(self):
        """Тест Б124: Отрицательный, метод create""" #разработать такой набор тестов, что ну и первое для каждого пути нашёлся тест из этого набора, то есть это первый вариант который как бы программа больше становится ну либо более простой вариант покрывающий для каждого оператора а это вершини операторы у нас это вершины для каждого оператора нашёлся тест выполняющий этот оператор. мы найдём все эти пути которые покрвывают это вершины, так у нас там было первое тестирование ... второе тестирование циклов ну вот обозначим н максимальное число выполнения итерация если оно неизвестно ну тогда бесконечно ну и ещё один параметр м количество ну число итераций для тестов то есть мы хотим разработать тесты ... которая определяет ... сколько итераций произойдёт ну и соответственно какие тесты можно предлагать пропуск цикла это по сути м равно нулю то есть разработать такой тест который бы пытался ни разу не выполнить указанный цикл оператор один а потом сразу девять то есть подобрать такие тесты чтобы программа вот так вот работала м равно 1 то есть одноразовое однократное выполенние ну аналогично м равно двум то есть мы на самом деле будем ещё изучать ошибки на границах то есть вот тут одна граница когда ... дальше ну давайте вот так вот то есть на самом деле число выполнения цикла ... вариант то есть типовой вариант то есть ожидаемое среднее к выполнению операций первоая группа из трёх ещё один класс получается м равно н плюс минус один ну минус понятно можно ещё и н записать на границе если это возможно мы пытаемся разработать тест ... то есть это получается близкий к максимуму интересный тест когда тест н плюс один когда больше максимлаьного когда мы пытаемся заставить работать программу ... мы пытаемся разработать тесты так чтобы специально найти ошибку так ну давайте запишем общие вещи разработка такого набора тестов чтобы покрыть все возможные вариенты повторения цикла, ну здесь таки принцип парето 
        data = {'answer_text': '', 'question': self.question.id}
        response = self.client.post('/api/answers/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_B125_retrieve_answer(self):
        """Тест Б125: Положительный, метод retrieve"""
        response = self.client.get(f'/api/answers/{self.answer.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.answer.id)

    def test_B126_retrieve_nonexistent_answer(self):
        """Тест Б126: Отрицательный, метод retrieve"""
        response = self.client.get('/api/answers/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_B127_update_answer(self):
        """Тест Б127: Положительный, метод update"""
        data = {'responder': self.user1.id, 'answer_text': 'Обновленный ответ', 'question': self.question.id}
        response = self.client.put(f'/api/answers/{self.answer.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['answer_text'], 'Обновленный ответ')

    def test_B128_update_invalid_answer(self):
        """Тест Б128: Отрицательный, метод update"""
        data = {'responder': self.user1.id, 'answer_text': '', 'question': self.question.id}
        response = self.client.put(f'/api/answers/{self.answer.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_B129_partial_update_answer(self):
        """Тест Б129: Положительный, метод partial_update"""
        data = {'answer_text': 'Частичный апдейт.'}
        response = self.client.patch(f'/api/answers/{self.answer.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['answer_text'], 'Частичный апдейт.')

    def test_B130_partial_update_invalid_answer(self):
        """Тест Б130: Отрицательный, метод partial_update"""
        data = {'answer_text': ''}
        response = self.client.patch(f'/api/answers/{self.answer.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_B131_delete_answer(self):
        """Тест Б131: Положительный, метод delete"""
        response = self.client.delete(f'/api/answers/{self.answer.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Answer.objects.filter(id=self.answer.id).exists())

    def test_B132_delete_nonexistent_answer(self):
        """Тест Б132: Отрицательный, метод delete"""
        response = self.client.delete('/api/answers/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)