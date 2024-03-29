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


def create_question(question_text, days=0, hours=0, minutes=0, seconds=0):
    """
    Create a question with the given "question_text", and pulished the given
    number of days, hours, minutes and seconds offset to now (negative for questions
    published in the past, possitive for questions that have not yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days, hours=hours, 
                                                minutes=minutes, seconds=seconds)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_questions(self):
        """
        Question with a pub_date in the future aren't displayed on index page
        """
        time = timezone.now() + datetime.timedelta(days=365)
        future_question = Question(question_text='¿Quién es el mejor Course Director de Platzi?', 
                                   pub_date=time)
        future_question.save()
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_questions(self):
        """
        Question with a pub_date in the past are displayed on index page
        """
        question = create_question('past question', days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past questions are displayed
        """
        past_question = create_question(question_text="Past question", days=-30)
        future_question = create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions
        """
        past_question1= create_question(question_text="Past question 1", days=-30)
        past_question2 = create_question(question_text="Past question 2", days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )

    def test_two_future_questions(self):
        """
        The Questions with a pub_date in the future aren't displayed on index page
        """
        future_question1= create_question(question_text="Future question 1", days=30)
        future_question2 = create_question(question_text="Future question 2", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context["latest_question_list"], [])


class QuestionDetailViewTest(TestCase):
    def test_future_question_not_found(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 
        error not found
        """
        future_question = create_question(question_text='Future question', days=30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question_displayed(self):
        """
        The detail view of a question with a pub_date in the past displays the question's text
        """
        past_question = create_question(question_text='Past question', days=-30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question)


class QuestionResultViewTest(TestCase):
    def test_result_future_question(self):
        """
        The result view of a question with a pub_date in the future returns a 404 
        error not found
        """
        future_question = create_question(question_text='Future question', days=30)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_result_past_question(self):
        """
        The results view of a question with a pub_date in the past show the question
        and its answers
        """
        past_question = create_question(question_text='Past question', days=-30)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question)
        