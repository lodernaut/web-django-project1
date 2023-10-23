from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_list_or_404
from django.views.generic import ListView

from recipes.models import Recipe


class RecipeListViewBase(ListView):
    # sobrescrevendo
    model = Recipe
    # 'context_object_name' é objeto que vai por padrão dentro do contexto é o 'recipes' de → {% for recipe in recipes %} # noqa:E501
    context_object_name = "recipes"
    # CBV já vem com uma paginação pronta.
    # paginate_by = 6
    ordering = ["id"]
    # queryset = Recipe.objects.filter(is_published=False).order_by("id")
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


# respondendo via JSON
class RecipeListViewHomeApi(RecipeListViewHome):
    # sobrescrevendo método que renderiza
    def render_to_response(self, context, **response_kwargs):
        recipes = context['recipes']
        data = []
        for recipe in recipes:
            recipe_data = {
                'id': recipe.id,
                'title': recipe.title,
                'description': recipe.description,
                'category': recipe.category.name if recipe.category else None,
                'cover': recipe.cover.url if recipe.cover else None,
                # Adicione outros campos que você deseja retornar
            }
            data.append(recipe_data)

        return JsonResponse(data, safe=False)


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
