from allauth.account.forms import LoginForm
from allauth.socialaccount.models import SocialAccount


def global_context(request):
    """
    Añade una instancia del formulario de login de allauth y la foto de perfil
    al contexto de cada plantilla.
    """
    profile_pic = None
    if request.user.is_authenticated:
        social = SocialAccount.objects.filter(
            user=request.user, provider="google").first()
        if social:
            profile_pic = social.extra_data.get("picture")

    return {
        'login_form': LoginForm(),
        'profile_pic': profile_pic,
    }
