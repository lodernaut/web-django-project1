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
    path("recipes/<int:id>/", views.RecipeDetailView.as_view(), name="recipe"),

    path(
        "recipes/api/v1/", views.RecipeListViewHomeApi.as_view(),
        name="recipes_api_home"),
    path(
        "recipes/api/v1/<int:id>/", views.RecipeDetailViewApi.as_view(),
        name="recipes_api_recipe"),
]
