from django.urls import path

from authors import views

app_name = "authors"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("register/create/", views.register_create, name="register_create"),
    path("login/", views.login_view, name="login"),
    path("login/create/", views.login_create, name="login_create"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        # vai está na recipe, da recipe recebe um id, do id faz um edit
        "dashboard/recipe/<int:id>/edit/",
        views.DashboardRecipe.as_view(), name="dashboard-recipe-edit"),
    path(
        "dashboard/recipe/new/", views.dashboard_new_recipe_view,
        name="dashboard-new-recipe"),
    path(
        "dashboard/recipe/new/create/", views.dashboard_new_recipe_create,
        name="dashboard-new-recipe-create"),
    path(
        "dashboard/recipe/delete/", views.dashboard_recipe_delete,
        name="dashboard-recipe-delete"),
]
