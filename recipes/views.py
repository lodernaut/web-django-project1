from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
# django está retornando renderizado a request e o caminho template
# HTTP REQUEST, TEMPLATE_NAME = caminho do template
def home(request):
    return render(request, "global/home.html", context= {
        "name": "Gabriel Lemos",
    }) 


# HTTP REQUEST
def sobre(request):
    return HttpResponse("sobre")


# HTTP REQUEST
def contato(request):
    return render(request, "tempdelete/temp.html")
    