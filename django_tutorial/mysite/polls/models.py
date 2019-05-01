import datetime
from django.db import models
from django.utils import timezone
# Create your models here.
# Model : DB에 어떤 데이터를 어떤 형식으로 저장할 것이냐?
# 모델이름 : 테이블이름
# 모델의 필드 : 컬럼 -> 데이터의 형식, 제약조건
# 정수, 실수, 글자, 길이없는 텍스트, 날짜
# 모델의 필드-> 프론트에서 사용하는 폼 태그의 종류와 제약조건
"""
Question
ID    Question_text   Pub_date
1      what is?        2019.04.23
2      who is?
3      How about?
create table Question question_text varchar(200),
pub_date datetime
"""
# 1. 모델만들기 : 필드의 종류와 제약조건 설정
# 2. 변경 사항 추적하기 : 모델을 읽어서 DB에 반영할 사항을 파일로 작성
# python manage.py makemigrations polls -> makemigrations [앱 이름]
# 3. 변경 사항 적용하기 : 변경 사항 파일을 읽어서 쿼리 실행
# python manage.py migrate polls 0001 -> migrate [앱이름] [마이그레이션 번호]

# 장고는 DB 의존성이 낮다. --> 특정 DB로부터 영향을 받지 않는다.
# ~에 대한 의존성이 높다. --> ~가 아니면 정상 동작하지 않는다.

# 어떤 쿼리가 실행될지 알고 싶다면
# python manage.py sqlmigrate polls 0001
# 어떤 쿼리가 실행될지 알고 싶다
# slow 쿼리인지 여부 확인
# 튜닝이 필요한 쿼리인지 여부 확인

# python manage.py migrate polls -> 데이터베이스 반영
# DBMS : SQLite Viewer
# MySQL : Workbench

class Question(models.Model):
    # 필드들은 옵션을 지정하지 않으면 무조건 필수 필드가 된다.
    # blank = True  ex) text의 경우 : ''
    # null = True   ex) text의 경우 : Null
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

