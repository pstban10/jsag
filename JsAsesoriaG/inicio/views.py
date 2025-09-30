from django.shortcuts import render, redirect, get_object_or_404
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from .forms import ProfileTypeForm, ClienteForm, ProveedorForm, PostulanteForm, CatalogoForm
from django.contrib import messages
from .models import Profile, Cliente, Proveedor, Postulante, Catalogo

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

@login_required
def invertir_view(request):
    return render(request, 'invertir.html')

@login_required
def proveedores_vip_view(request):
    return render(request, 'proveedores_vip.html')

@login_required
def asesoria_legal_view(request):
    return render(request, 'asesoria_legal.html')

@login_required
def mi_catalogo_view(request):
    try:
        proveedor = request.user.proveedor
    except Proveedor.DoesNotExist:
        return redirect('index')

    catalogo = Catalogo.objects.filter(proveedor=proveedor)
    context = {
        'catalogo': catalogo
    }
    return render(request, 'mi_catalogo.html', context)

@login_required
def agregar_producto_view(request):
    try:
        proveedor = request.user.proveedor
    except Proveedor.DoesNotExist:
        return redirect('index')

    if request.method == 'POST':
        form = CatalogoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.proveedor = proveedor
            producto.save()
            return redirect('mi_catalogo')
    else:
        form = CatalogoForm()

    context = {
        'form': form
    }
    return render(request, 'editar_catalogo.html', context)

@login_required
def editar_producto_view(request, pk):
    try:
        proveedor = request.user.proveedor
    except Proveedor.DoesNotExist:
        return redirect('index')

    producto = get_object_or_404(Catalogo, pk=pk, proveedor=proveedor)

    if request.method == 'POST':
        form = CatalogoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('mi_catalogo')
    else:
        form = CatalogoForm(instance=producto)

    context = {
        'form': form
    }
    return render(request, 'editar_catalogo.html', context)

@login_required
def eliminar_producto_view(request, pk):
    try:
        proveedor = request.user.proveedor
    except Proveedor.DoesNotExist:
        return redirect('index')

    producto = get_object_or_404(Catalogo, pk=pk, proveedor=proveedor)
    if request.method == 'POST':
        producto.delete()
        return redirect('mi_catalogo')
    
    context = {
        'producto': producto
    }
    return render(request, 'eliminar_producto_confirm.html', context)

@login_required
def banco_cv_view(request):
    return render(request, 'banco_cv.html')

@login_required
def mi_perfil_view(request):
    return render(request, 'mi_perfil.html')
