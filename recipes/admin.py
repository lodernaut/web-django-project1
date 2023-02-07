from django.contrib import admin

from .models import Category, Recipe

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)  # decorator
class RecipeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)  # 1º model, 2º category
