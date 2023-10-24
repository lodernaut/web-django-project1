from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.generic import DetailView

from recipes.models import Recipe


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = "recipe"
    pk_url_kwarg = "id"
    template_name = "recipes/pages/recipe-view.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        cd = super().get_context_data(*args, **kwargs)
        cd.update({
            "is_detail_page": True, })
        return cd


class RecipeDetailViewApi(RecipeDetailView):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_object()
        # Converta o objeto 'recipe' em um dicionário
        recipe_dict = {
            "title": recipe.title,
            "description": recipe.description,
            "category": recipe.category.name if recipe.category else None,
            "author": recipe.author.get_full_name() if recipe.author else "Autor Desconhecido",
            'preparation_time': recipe.preparation_time,
            'preparation_time_unit': recipe.preparation_time_unit,
            'cover': self.request.build_absolute_uri(recipe.cover.url) if recipe.cover else None,
            # Adicione todos os outros campos que você deseja retornar aqui
        }
        return JsonResponse(recipe_dict)


class RecipeDetailViewApix(RecipeDetailView):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()["recipe"]  # model
        recipe_dict = model_to_dict(recipe)

        # Lógica
        recipe_dict["created_at"] = str(recipe.created_at)

        del recipe_dict["is_published"]

        if recipe_dict.get("cover"):
            # recipe_dict["cover"] = recipe_dict["cover"].url
            # or

            # Passando url absoluta + dicionário
            recipe_dict["cover"] = self.request.build_absolute_uri(
                recipe_dict["cover"].url)
        else:
            recipe_dict["cover"] = ""

        return JsonResponse(recipe_dict, safe=False,)
