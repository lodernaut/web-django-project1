from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
# HTTP REQUEST
def home(request):
    return render(request, "home.html" )


# HTTP REQUEST
def sobre(request):
    return HttpResponse("sobre")


# HTTP REQUEST
def contato(request):
    return HttpResponse("contato")
