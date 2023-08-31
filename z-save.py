from django.contrib import admin

from .models import Category, Recipe

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)  # decorator
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at", "is_published"]
    list_display_links = list_display  # adicionando link
    # adicionando campos de busca/ definindo quais campos a ser buscado
    search_fields = "id", "title", "description", "slug", "preparation_step"
    # adicionando filter
    list_filter = ("category", "authors", "is_published",
                   "preparation_step_is_html")


admin.site.register(Category, CategoryAdmin)  # 1º model, 2º category
