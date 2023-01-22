from django.shortcuts import render

# Create your views here.


# http Request <- return http Response
def home(request):
    return render(request, "recipes/pages/home.html", context={
        "name": "Gabriel Lemos",
    })
