from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe


class DashboardRecipe(View):
    def get_recipe(self, id):
        recipe = None
        if id:
            recipe = Recipe.objects.get(
                is_published=False, author=self.request.user, pk=id)  # utilizando self.request da própria classe
            if not recipe:
                raise Http404()
        return recipe

    def render_recipe(self, form):
        return render(
            self.request, "authors/pages/dashboard_recipe.html", context={
                "form": form,
            })

    def get(self, *args, **kwargs):
        recipe = self.get_recipe(kwargs.get("id"))
        form = AuthorRecipeForm(
            instance=recipe  # instance informa qual instancia será renderizada
        )
        return self.render_recipe(form)

    def post(self, request, id):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(
            request.POST or None,  # passando post para dentro do form se estiver vazio passa None
            files=request.FILES or None,
            instance=recipe,
        )
        if form.is_valid():
            # tentando salvar o form válido, 'quebra se estiver faltando dados'
            recipe = form.save(commit=False)
            recipe.author = request.user  # garantindo que author de recipe é request.user
            recipe.preparation_step_is_html = False
            recipe.is_published = False
            recipe.save()

            messages.success(
                request, "Your recipe has been successfully saved.")
            return redirect(reverse("authors:dashboard"))

        return self.render_recipe(form)
