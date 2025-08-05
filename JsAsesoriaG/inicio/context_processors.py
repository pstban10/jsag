from allauth.socialaccount.models import SocialAccount
from .models import Profile


def user_context(request):
    user_type = None
    profile_pic = None

    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        if profile:
            user_type = profile.user_type

        # Imagen de Google
        social = SocialAccount.objects.filter(
            user=request.user, provider="google").first()
        if social:
            profile_pic = social.extra_data.get("picture")
        else:
            # Si hay una foto local según el tipo de usuario
            if user_type == 'cliente':
                profile_pic = getattr(
                    request.user.cliente, 'foto_perfil', None)
            elif user_type == 'proveedor':
                profile_pic = getattr(
                    request.user.proveedor, 'foto_perfil', None)
            elif user_type == 'postulante':
                profile_pic = getattr(
                    request.user.postulante, 'foto_perfil', None)

    return {
        'user_type': user_type,
        'profile_pic': profile_pic,
    }

