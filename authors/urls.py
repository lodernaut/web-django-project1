from django.urls import path

from . import views

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
        views.dashboard_recipe_edit, name="dashboard-recipe-edit"),
    path(
        "dashboard/recipe/new/", views.dashboard_new_recipe_view,
        name="dashboard-new-recipe"),
    path(
        "dashboard/recipe/new/create/", views.dashboard_new_recipe_create,
        name="dashboard-new-recipe-create"),
    path(
        "dashboard/recipe/<int:id>/delete/", views.dashboard_recipe_delete,
        name="dashboard-recipe-delete"),
]
