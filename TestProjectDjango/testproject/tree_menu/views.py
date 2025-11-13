from django.shortcuts import render
from django.http import Http404, HttpRequest, HttpResponse
from .models import MenuItem

def home_page(request):
    """Главная страница"""

    return render(request, 'tree_menu/base.html')


def dynamic_page(request: HttpRequest, path: str = "") -> HttpResponse:
    """Универсальный обработчик страниц, создаваемых через админку."""

    current_path = f"/{path.strip('/')}/"

    menu_item = MenuItem.objects.filter(url=current_path).first()
    if menu_item is None:
        raise Http404("Раздел не найден в меню")

    context = {
        "menu_item": menu_item,
    }

    return render(request, "tree_menu/dynamic_page.html", context)
