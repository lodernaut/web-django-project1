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
