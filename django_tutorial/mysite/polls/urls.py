from django.urls import path

from . import views

urlpatterns = [
    #path('url pattern', view, name='url
    path('', views.index, name='index'),
    path('welcome/', views.welcome, name = 'welcome'),
    # ex: /polls/5/
    # urlpattern : index/
    # urlpattern2 : <question_id>/   --> view.py 함수의 매개변수명과 동일
    # urlpattern3 : <int:question_id>/
    # <slug:category_name>/<int:product_id>/
    # <int:password>/view/

    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

