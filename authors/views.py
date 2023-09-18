from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe

from .forms import LoginForm, RegisterForm


# Create your views here.
def register_view(request):
    register_form_data = request.session.get(
        "register_form_data", None)  # padrão já é None
    form = RegisterForm(register_form_data)

    return render(
        request, "authors/pages/register_view.html", {
            "form": form,
            "form_action": reverse("authors:register_create"),
        })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    # Salvando dicionário do POST inteiro
    request.session["register_form_data"] = POST
    form = RegisterForm(POST)

    if form.is_valid():  # se o formulário é valido
        user = form.save(commit=False)
        # configurando password antes de salvar na base de dados
        user.set_password(user.password)
        user.save()
        messages.success(request, "Your user is created, please log in.")

        # deletando/limpando chave do dicionário
        del (request.session["register_form_data"])
        return redirect(reverse("authors:login"))
    return redirect("authors:register")


def login_view(request):
    form = LoginForm()
    return render(request, "authors/pages/login.html", {
        "form": form,
        "form_action": reverse("authors:login_create"),
    })


def login_create(request):
    if not request.POST:
        raise Http404()  # se não for POST levanta 404

    form = LoginForm(request.POST)
    if form.is_valid():  # formulário válido não quer dizer que os dados que estão nesse formulário são válidos mas sim que usuário cumpriu com as regras do formulário.
        authenticated_user = authenticate(
            username=form.cleaned_data.get("username", ""),
            password=form.cleaned_data.get("password", ""),)

        if authenticated_user is not None:
            messages.success(request, "Your are logged in.")
            login(request, authenticated_user)
        else:
            messages.error(request, "Invalid credentials.")
    else:
        messages.error(request, "Invalid username or password.")
    return redirect(reverse("authors:dashboard"))


# 1º Usuário estando logado entra nesse campo ↓ ↓
@login_required(login_url="authors:login", redirect_field_name="next")
def logout_view(request):
    if not request.POST:  # 2º precisa se um POST (form) para entrar
        return redirect(reverse("authors:login"))

    # 3º Usuário que visualizando o form necessita se o usuário logado (usuário logado vai se conferido,)
    if request.POST.get("username") != request.user.username:
        messages.error(request, "Invalid logout user")
        print("invalid user name", request.POST, request.user)
        return redirect(reverse("authors:login"))

    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect(reverse("authors:login"))


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False, author=request.user)
    return render(request, "authors/pages/dashboard.html", context={
        "recipes": recipes,
    })


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.get(
        is_published=False, author=request.user, pk=id)
    if not recipe:
        raise Http404()
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

        messages.success(request, "Your recipe has been successfully saved.")
        return redirect(reverse("authors:dashboard"))

    return render(request, "authors/pages/dashboard_recipe.html", context={
        "form": form,
    })


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_new_recipe_view(request):
    register_form_data = request.session.get(
        "register_form_data", None)
    form = AuthorRecipeForm(
        register_form_data,
        files=request.FILES or None,
    )

    return render(
        request, "authors/pages/dashboard_add_new_recipe.html", context={
            "form": form,
            "form_action": reverse("authors:dashboard-new-recipe-create"),
        })


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_new_recipe_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session["register_form_data"] = POST
    form = AuthorRecipeForm(POST)

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_step_is_html = False
        recipe.is_published = False
        recipe.slug = recipe.title
        recipe.save()
        messages.success(request, "Your recipe has been saved")
        del (request.session["register_form_data"])
        return redirect(reverse("authors:dashboard"))
    messages.error(request, "houve algum erro")

    return redirect(reverse("authors:dashboard-new-recipe"))


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404()

    id = request.POST.get("id")

    recipe = Recipe.objects.get(
        # check se receita está publicada, author e id
        is_published=False, author=request.user, pk=id)
    if not recipe:
        raise Http404()
    recipe.delete()
    messages.info(request, "Excluded recipe.")
    return redirect(reverse("authors:dashboard"))
