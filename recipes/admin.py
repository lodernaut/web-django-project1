from django.contrib import admin

from .models import Category, Recipe

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)  # decorator
class RecipeAdmin(admin.ModelAdmin):
    list_display = "id", "title", "author", "created_at", "is_published",
    list_display_links = [
        "id", "title", "author", "created_at"]  # adicionando link's
    # adicionando campos de busca/ definindo quais campos a ser buscado
    search_fields = "id", "title", "description", "slug", "preparation_step",
    # adicionando filter
    list_filter = [
        "is_published", "category", "author", "preparation_step_is_html"]
    # list_per_page = 5  # Caso queira controlar quantidade de  visível por pág
    list_editable = "is_published",
    # ordering = "id",  # se quiser ordenar


admin.site.register(Category, CategoryAdmin)  # 1º model, 2º category
