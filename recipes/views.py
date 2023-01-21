from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


# http Request <- return http Response
def home(request):
    return render(request, "global/home.html")


def about(request):
    return HttpResponse("TESTE RETORNO sobre")


def contact(Requrequestest):
    return HttpResponse("TESTE RETORNO contato")
