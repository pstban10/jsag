from django.shortcuts import render, redirect, get_object_or_404
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Cliente, Proveedor, Postulante, Producto, OfertaEmpleo, Postulacion
from .forms import ProfileTypeForm, ClienteForm, ProveedorForm, PostulanteForm, ProductoForm, OfertaEmpleoForm, PostulacionForm
from functools import wraps

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Asumiendo que el perfil siempre existe para un usuario logueado
            if not hasattr(request.user, 'profile') or request.user.profile.user_type != role:
                return redirect('/') # Redirigir si no tiene el rol
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

@login_required
def profile_completion_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if profile.is_profile_complete:
        return redirect('/')

    if request.method == 'POST':
        if not profile.user_type:
            type_form = ProfileTypeForm(request.POST, instance=profile)
            if type_form.is_valid():
                type_form.save()
                return redirect('profile_completion')
        else:
            form_class_map = {
                'cliente': ClienteForm,
                'proveedor': ProveedorForm,
                'postulante': PostulanteForm,
            }
            model_class_map = {
                'cliente': Cliente,
                'proveedor': Proveedor,
                'postulante': Postulante,
            }
            model = model_class_map.get(profile.user_type)
            form_class = form_class_map.get(profile.user_type)
            
            instance, _ = model.objects.get_or_create(user=request.user)
            form = form_class(request.POST, request.FILES, instance=instance)
            
            if form.is_valid():
                form.save()
                profile.is_profile_complete = True
                profile.save()
                messages.success(request, '¡Tu perfil ha sido completado con éxito!')
                return redirect('/')
    else:
        if not profile.user_type:
            form = ProfileTypeForm(instance=profile)
        else:
            form_class_map = {
                'cliente': ClienteForm,
                'proveedor': ProveedorForm,
                'postulante': PostulanteForm,
            }
            model_class_map = {
                'cliente': Cliente,
                'proveedor': Proveedor,
                'postulante': Postulante,
            }
            model = model_class_map.get(profile.user_type)
            form_class = form_class_map.get(profile.user_type)
            instance, _ = model.objects.get_or_create(user=request.user)
            form = form_class(instance=instance)

    context = {
        'form': form,
        'user_type': profile.user_type
    }
    return render(request, 'account/profile_completion.html', context)

@login_required
def index(request):
    if not request.user.profile.is_profile_complete:
        return redirect('profile_completion')
    
    user_type = request.user.profile.user_type
    if user_type == 'cliente':
        return redirect('cliente_dashboard')
    elif user_type == 'proveedor':
        return redirect('proveedor_dashboard')
    elif user_type == 'postulante':
        return redirect('postulante_dashboard')
    
    # Fallback para usuarios sin un rol definido o para la portada principal
    return render(request, 'index.html')

@login_required
def profile_view(request):
    profile = request.user.profile
    form_class_map = {
        'cliente': (Cliente, ClienteForm),
        'proveedor': (Proveedor, ProveedorForm),
        'postulante': (Postulante, PostulanteForm),
    }
    model, form_class = form_class_map.get(profile.user_type)
    instance = get_object_or_404(model, user=request.user)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado con éxito!')
            return redirect('profile')
    else:
        form = form_class(instance=instance)

    context = {
        'form': form,
        'profile': instance
    }
    return render(request, 'profile.html', context)

# --- Dashboards ---
@login_required
@role_required('cliente')
def cliente_dashboard(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    ofertas = OfertaEmpleo.objects.filter(cliente=cliente)
    return render(request, 'cliente/dashboard.html', {'ofertas': ofertas})

@login_required
@role_required('proveedor')
def proveedor_dashboard(request):
    proveedor = get_object_or_404(Proveedor, user=request.user)
    productos = Producto.objects.filter(proveedor=proveedor)
    return render(request, 'proveedor/dashboard.html', {'productos': productos})

@login_required
@role_required('postulante')
def postulante_dashboard(request):
    postulante = get_object_or_404(Postulante, user=request.user)
    postulaciones = Postulacion.objects.filter(postulante=postulante)
    return render(request, 'postulante/dashboard.html', {'postulaciones': postulaciones})

# --- CRUD de Productos (Proveedor) ---
@login_required
@role_required('proveedor')
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.proveedor = request.user.proveedor
            producto.save()
            messages.success(request, 'Producto creado con éxito.')
            return redirect('proveedor_dashboard')
    else:
        form = ProductoForm()
    return render(request, 'proveedor/crear_producto.html', {'form': form})

@login_required
@role_required('proveedor')
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, proveedor__user=request.user)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado con éxito.')
            return redirect('proveedor_dashboard')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'proveedor/editar_producto.html', {'form': form})

@login_required
@role_required('proveedor')
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, proveedor__user=request.user)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado con éxito.')
        return redirect('proveedor_dashboard')
    return render(request, 'proveedor/eliminar_producto.html', {'producto': producto})

# --- CRUD de Ofertas (Cliente) ---
@login_required
@role_required('cliente')
def crear_oferta(request):
    if request.method == 'POST':
        form = OfertaEmpleoForm(request.POST)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.cliente = request.user.cliente
            oferta.save()
            messages.success(request, 'Oferta de empleo creada con éxito.')
            return redirect('cliente_dashboard')
    else:
        form = OfertaEmpleoForm()
    return render(request, 'cliente/crear_oferta.html', {'form': form})

@login_required
@role_required('cliente')
def editar_oferta(request, pk):
    oferta = get_object_or_404(OfertaEmpleo, pk=pk, cliente__user=request.user)
    if request.method == 'POST':
        form = OfertaEmpleoForm(request.POST, instance=oferta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oferta de empleo actualizada con éxito.')
            return redirect('cliente_dashboard')
    else:
        form = OfertaEmpleoForm(instance=oferta)
    return render(request, 'cliente/editar_oferta.html', {'form': form})

@login_required
@role_required('cliente')
def eliminar_oferta(request, pk):
    oferta = get_object_or_404(OfertaEmpleo, pk=pk, cliente__user=request.user)
    if request.method == 'POST':
        oferta.delete()
        messages.success(request, 'Oferta de empleo eliminada con éxito.')
        return redirect('cliente_dashboard')
    return render(request, 'cliente/eliminar_oferta.html', {'oferta': oferta})

# --- Lógica de Postulantes ---
@login_required
@role_required('postulante')
def lista_ofertas(request):
    ofertas = OfertaEmpleo.objects.filter(activa=True).order_by('-fecha_publicacion')
    return render(request, 'postulante/lista_ofertas.html', {'ofertas': ofertas})

@login_required
@role_required('postulante')
def detalle_oferta(request, pk):
    oferta = get_object_or_404(OfertaEmpleo, pk=pk, activa=True)
    postulacion_existente = Postulacion.objects.filter(oferta=oferta, postulante__user=request.user).exists()
    if request.method == 'POST':
        if not postulacion_existente:
            form = PostulacionForm(request.POST)
            if form.is_valid():
                postulacion = form.save(commit=False)
                postulacion.postulante = request.user.postulante
                postulacion.oferta = oferta
                postulacion.save()
                messages.success(request, 'Te has postulado con éxito.')
                return redirect('postulante_dashboard')
        else:
            messages.error(request, 'Ya te has postulado a esta oferta.')
            return redirect('detalle_oferta', pk=pk)
    else:
        form = PostulacionForm()
    return render(request, 'postulante/detalle_oferta.html', {'oferta': oferta, 'form': form, 'postulacion_existente': postulacion_existente})

# --- Vistas Estáticas ---
def somos(request):
    return render(request, "somos.html")

def servicios(request):
    return render(request, "servicios.html")

def finance(request):
    return render(request, 'finanzas.html')

def gestion(request):
    return render(request, 'gestion.html')

def profile(request):
    return render(request, "profile.html")