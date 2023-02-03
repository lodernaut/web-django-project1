from django.shortcuts import render

# Create your views here.


# http Request <- return http Response
def home(request):
    return render(request, "recipes/pages/home.html")


def recipe(request, id):
    return render(request, "recipes/pages/recipe-view.html")
