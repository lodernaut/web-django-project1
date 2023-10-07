from django.urls import path

from recipes import views

# recipes:recipes
app_name = "recipes"

# http Request <- return http Response
urlpatterns = [
    # domínio/recipes  → # home
    path("", views.RecipeListViewBase.as_view(), name="home"),
    # passando paramento <id> → para → views.recipe
    path("recipes/search/", views.search, name="search"),
    path(
        "recipes/category/<int:category_id>/",
        views.category, name="category"),
    path("recipes/<int:id>/", views.recipe, name="recipe"),
]
