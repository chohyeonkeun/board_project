"""
import 구문 순서
1. 파이썬 기본 모듈들  ex) import random (한줄 띄고) import os
2. 3rd-party 모듈들
3. 내가 만든 모듈
"""

from django.contrib import admin

from .models import Question, Choice
# Register your models here.

admin.site.register(Question)
admin.site.register(Choice)