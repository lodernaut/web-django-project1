from django.urls import path

from . import views

# recipes:recipes
app_name = "recipes"

# http Request <- return http Response
urlpatterns = [
    path("", views.home, name="home"),  # domínio/recipes  → # home
    # passando paramento <id> → para → views.recipe
    path("recipes/category/<int:category_id>/",
         views.category, name="category"),
    path("recipes/<int:id>/", views.recipe, name="recipe"),
]
