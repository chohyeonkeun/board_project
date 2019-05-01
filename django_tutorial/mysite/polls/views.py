from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.template import loader

from django.http import Http404

from django.shortcuts import render

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # 템플릿 시스템 (화면에 보여져야 하는 html 코드를 장고로 넣어놓는 것이 아니라 따로 폴더에 넣어 놓는 시스템)
    # render(request, 템플릿, 템플릿 변수)
    return HttpResponse(template.render(context, request))


# 뷰 : 클래스형 뷰, 함수형 뷰
# def [뷰이름](request):
#   return HttpResponse('화면에 출력될 내용')
def welcome(request):
    return HttpResponse('Welcome first django page')


# detail 뷰 : 매개변수가 question_id를 받는다.
# 함수형 뷰는 기본적으로 request 라는 매개변수를 받는다.
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)