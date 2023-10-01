from django.contrib.auth.models import User  # user do próprio django.
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=65)

    # magic method
    def __str__(self):
        return self.name


class Recipe(models.Model):  # herdando de models.Model
    # campo de texto com máximo de 65 caracteres.
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=False)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_step = models.TextField()  # campo → text-area
    # campo de escolha → startando como False. cspell:disable-line
    preparation_step_is_html = models.BooleanField(default=False)

    # auto_now_add=True → gera data apenas na criação.
    created_at = models.DateTimeField(auto_now_add=True)

    # auto_now=True → gera data apenas em atualização.
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    # %Y/%m/%d/ → registrando data de upload.
    cover = models.ImageField(
        upload_to="recipes/covers/%Y/%m/%d/", blank=True, default="")

    # criando ligação entre 'Category e Recipe'
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        blank=True, default=None)

    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    # magic method
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "recipes:recipe", kwargs={"id": self.id})  # type: ignore
