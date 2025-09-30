# En tu_app/context_processors.py

from allauth.account.forms import LoginForm


def add_login_form_to_context(request):
    """
    Añade una instancia del formulario de login de allauth al contexto
    de cada plantilla, para que esté disponible en el modal de base.html.
    """
    return {
        'login_form': LoginForm(),
    }
