from django.urls import path

from . import views

# recipes-recipe
app_name = "recipes"

urlpatterns = [
    path("", views.home, name="recipes-home"),  # Home
    # recipe, criando caminho dinâmico → name="recipes-recipe"
    path("recipes/<int:id>/", views.recipe, name="recipes-recipe"),
]
