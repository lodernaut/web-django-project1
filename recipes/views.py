from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


# http Request <- return http Response
def home(Request):
    return HttpResponse("TESTE RETORNO home")


def about(Request):
    return HttpResponse("TESTE RETORNO sobre")


def contact(Request):
    return HttpResponse("TESTE RETORNO contato")
