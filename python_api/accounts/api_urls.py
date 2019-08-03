from django.urls import path
from .views import *

urlpatterns = [
    path('', AccountLCAPI.as_view()),
    path('<int:pk>/', AccountRUDAPI.as_view()),
]