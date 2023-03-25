import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question

# se testean usalmente Models o Vistas

class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text='¿Quién es el mejor Course Director de Platzi?', 
                                   pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns False for questions whose pub_date is greater than 24 hours old"""
        time = timezone.now() - datetime.timedelta(days=3)
        past_question = Question(question_text='¿Quién es el mejor Course Director de Platzi?', 
                                   pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)

    
    def test_was_published_recently_with_present_questions(self):
        """was_published_recently returns True for questions whose pub_date is less than 24 hours old"""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        present_question = Question(question_text='¿Quién es el mejor Course Director de Platzi?', 
                                   pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)


class QuestionIndexViewTest(TestCase):
    
    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_future_questions(self):
        """the future questions are not visible"""
        time = timezone.now() + datetime.timedelta(days=365)
        future_question = Question(question_text='¿Quién es el mejor Course Director de Platzi?', 
                                   pub_date=time)
        future_question.save()
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
