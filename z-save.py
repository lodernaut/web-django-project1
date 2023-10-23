
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404
from django.views.generic import ListView

from recipes.models import Recipe


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = "recipes"
    ordering = ["id"]
    template_name = "recipes/pages/home.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        cd = super().get_context_data(*args, **kwargs)
        recipes = self.get_queryset()

        paginator = Paginator(recipes, 9)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        cd.update({
            "recipes": page_obj,
            "page_obj": page_obj,
        })
        return cd


class RecipeListViewHome(RecipeListViewBase):
    template_name = "recipes/pages/home.html"


class RecipeListViewCategory(RecipeListViewBase):
    template_name = "recipes/pages/category.html"
    ordering = ["-id"]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = get_list_or_404(
            qs.filter(category__id=self.kwargs.get("category_id")))
        return qs

    def get_context_data(self, *args, **kwargs):
        cd = super().get_context_data(*args, **kwargs)
        recipes = self.get_queryset()
        cd.update({
            "title": f"{recipes[0].category.name}"
        })
        return cd


class RecipeListViewSearch(RecipeListViewBase):
    template_name = "recipes/pages/search.html"
    ordering = ["-id"]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get("q", "").strip()
        if not search_term:
            raise Http404()
        qs = qs.filter(
            Q
            (
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term) |
                Q(slug__icontains=search_term)
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        cd = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get("q", "").strip()
        cd.update({
            "page_title": f"Search for '{search_term}'",
            "search_term": search_term,
            "add_url_query": f"&q={search_term}",
        })
        return cd
