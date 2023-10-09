from django.urls import path

from recipes import views

# recipes:recipes
app_name = "recipes"

# http Request <- return http Response
urlpatterns = [
    # domínio/recipes  → # home
    path("", views.RecipeListViewHome.as_view(), name="home"),
    # passando paramento <id> → para → views.recipe
    path("recipes/search/", views.RecipeListViewSearch.as_view(), name="search"),
    path(
        "recipes/category/<int:category_id>/",
        views.RecipeListViewCategory.as_view(), name="category"),
    path("recipes/<int:id>/", views.recipe, name="recipe"),
]
