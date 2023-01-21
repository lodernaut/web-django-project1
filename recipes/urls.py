from django.urls import path

from recipes.views import about, contact, home

# http Request <- return http Response
urlpatterns = [
    path("", home),  # domínio/recipes  → # home
    path("about/", about),
    path("contact/", contact),  # /contact/

]
