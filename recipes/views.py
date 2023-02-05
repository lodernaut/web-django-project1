from django.shortcuts import render

from utils.recipes.factory import make_recipe

# Create your views here.


# http Request <- return http Response
def home(request):
    return render(request, "recipes/pages/home.html", context={
        # list comprehension. ↓
        "recipes": [make_recipe for _ in range(11)],
    })


def recipe(request, id):
    return render(request, "recipes/pages/recipe-view.html", context={
        "recipe": make_recipe(),
    })
