from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from .forms import ProfileTypeForm, ClienteForm, ProveedorForm, PostulanteForm
from django.contrib import messages
from .models import Profile, Cliente, Proveedor, Postulante

@login_required
def profile_completion_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if profile.is_profile_complete:
        return redirect('/')

    if request.method == 'POST':
        # Si el usuario aún no ha seleccionado un tipo de perfil
        if not profile.user_type:
            type_form = ProfileTypeForm(request.POST, instance=profile)
            if type_form.is_valid():
                type_form.save()
                # Redirigir a la misma vista para completar el perfil específico
                return redirect('profile_completion')
        else:
            # El usuario ya tiene un tipo de perfil, ahora completa los detalles
            if profile.user_type == 'cliente':
                instance, _ = Cliente.objects.get_or_create(user=request.user)
                form = ClienteForm(request.POST, request.FILES, instance=instance)
            elif profile.user_type == 'proveedor':
                instance, _ = Proveedor.objects.get_or_create(user=request.user)
                form = ProveedorForm(request.POST, request.FILES, instance=instance)
            else: # Postulante
                instance, _ = Postulante.objects.get_or_create(user=request.user)
                form = PostulanteForm(request.POST, request.FILES, instance=instance)

            if form.is_valid():
                form.save()
                profile.is_profile_complete = True
                profile.save()
                messages.success(request, '¡Tu perfil ha sido completado con éxito!')
                return redirect('/')
    else:
        # Si el usuario aún no ha seleccionado un tipo de perfil, muestra el formulario de tipo
        if not profile.user_type:
            form = ProfileTypeForm(instance=profile)
        else:
            # Si ya tiene un tipo, muestra el formulario correspondiente
            if profile.user_type == 'cliente':
                instance, _ = Cliente.objects.get_or_create(user=request.user)
                form = ClienteForm(instance=instance)
            elif profile.user_type == 'proveedor':
                instance, _ = Proveedor.objects.get_or_create(user=request.user)
                form = ProveedorForm(instance=instance)
            else: # Postulante
                instance, _ = Postulante.objects.get_or_create(user=request.user)
                form = PostulanteForm(instance=instance)

    context = {
        'form': form,
        'user_type': profile.user_type
    }
    return render(request, 'account/profile_completion.html', context)

@login_required
def cliente_dashboard(request):
    return render(request, 'cliente/dashboard.html')

@login_required
def proveedor_dashboard(request):
    return render(request, 'proveedor/dashboard.html')

@login_required
def postulante_dashboard(request):
    return render(request, 'postulante/dashboard.html')

def index(request):
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        if not profile.is_profile_complete:
            return redirect('profile_completion')
        else:
            if profile.user_type == 'cliente':
                return redirect('cliente_dashboard')
            elif profile.user_type == 'proveedor':
                return redirect('proveedor_dashboard')
            elif profile.user_type == 'postulante':
                return redirect('postulante_dashboard')

    return render(request, 'index.html')


def somos(request):
    return render(
        request,
        "somos.html"
    )


def servicios(request):
    return render(
        request,
        "servicios.html"
    )


def index(request):
    profile_pic = None
    if request.user.is_authenticated:
        social = SocialAccount.objects.filter(
            user=request.user, provider="google").first()
        if social:
            profile_pic = social.extra_data.get("picture")
    return render(
        request,
        'index.html',
        {"profile_pic": profile_pic}
    )


def finance(request):
    return render(
        request,
        'finanzas.html'
    )


def gestion(request):
    return render(
        request,
        'gestion.html'
    )


def profile(request):

    return render(
        request,
        "profile.html"
    )
