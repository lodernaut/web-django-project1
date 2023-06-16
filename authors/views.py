from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

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
    login_url = reverse("authors:login")
    if form.is_valid():  # formulário válido não quer dizer que os dados que estão nesse formulário são válidos mas sim que usuário cumpriu com as regras do formulário.
        authenticated_user = authenticate(
            username=form.cleaned_data.get("username", ""),
            password=form.cleaned_data.get("password", ""),)

        if authenticated_user is not None:
            login(request, authenticated_user)
            messages.success(request, "Your are logged in.")

        else:
            messages.error(request, "Invalid credentials.")
    else:
        messages.error(request, "Invalid username or password.")
    return redirect(login_url)
