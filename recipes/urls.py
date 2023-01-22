from django.urls import path

from recipes.views import home

# http Request <- return http Response
urlpatterns = [
    path("", home),  # domínio/recipes  → # home


]
