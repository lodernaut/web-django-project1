from django.shortcuts import render


# Create your views here.
def register_view(request):
    # renderizando template
    return render(request, "authors/pages/register_view.html")
