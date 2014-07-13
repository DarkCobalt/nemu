from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required()
def hello(request):
    return HttpResponse('hello!')

@login_required()
def index(request):
    return render(request, 'workflow/index.html')