from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import LoginForm, RegisterForm
from recipes.models import Recipe


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
    if form.is_valid():  # formulário válido não quer dizer que os dados que estão nesse formulário são válidos mas sim que usuário cumpriu com as regras do formulário. # noqa:E501
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

    # 3º Usuário que visualizando o form necessita se o usuário logado (usuário logado vai se conferido,) # noqa:E501
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
