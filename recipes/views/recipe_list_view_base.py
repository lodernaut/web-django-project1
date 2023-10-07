
import os

from django.db.models.query import QuerySet
from django.views.generic import ListView

from recipes.models import Recipe
from utils.pagination import make_pagination


class RecipeListViewBase(ListView):
    # sobrescrevendo
    model = Recipe
    # 'context_object_name' é objeto que vai por padrão dentro do contexto é o 'recipes' de → {% for recipe in recipes %} # noqa:E501
    context_object_name = "recipes"
    # CBV já vem com uma paginação pronta.
    # paginate_by = 6
    ordering = ["-id"]
    # queryset = Recipe.objects.filter(is_published=False).order_by("id")
    template_name = "recipes/pages/home.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        PER_PAGE_HOME = int(os.environ.get("PER_PAGE_HOME", 6))
        cd = super().get_context_data(*args, **kwargs)
        page_object, pagination_range = make_pagination(
            self.request, cd.get("recipes"), PER_PAGE_HOME)
        cd.update({
            "recipes": page_object,
            "pagination_range": pagination_range
        })

        return cd
