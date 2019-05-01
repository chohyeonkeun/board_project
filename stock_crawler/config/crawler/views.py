from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def crawling(requests):
    return HttpResponse("Let's do crawling")

