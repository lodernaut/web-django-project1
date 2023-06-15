from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import RegisterForm


# Create your views here.
def register_view(request):
    register_form_data = request.session.get(
        "register_form_data", None)  # padrão já é None
    form = RegisterForm(register_form_data)

    return render(
        request, "authors/pages/register_view.html", {
            "form": form,
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
