from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Question


def index(request):
    latest_question_list = Question.objects.all()
    context = {
        "latest_question_list": latest_question_list
    }
    return render(request=request, template_name='polls/index.html',
                context=context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {
        'question': question
    })


def results(request, question_id):
    return HttpResponse(f'Estás viendo los resultados de la pregunta número {question_id}')


def vote(request, question_id):
    return HttpResponse(f'Estás votando a la pregunta número {question_id}')
