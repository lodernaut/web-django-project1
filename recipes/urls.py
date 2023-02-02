from django.urls import path

from . import views

# http Request <- return http Response
urlpatterns = [
    path("", views.home),  # domínio/recipes  → # home
    # passando paramento <id> → para → views.recipe
    path("recipes/<int:id>/", views.recipe),
]
