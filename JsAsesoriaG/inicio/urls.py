
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('profile/complete/', views.profile_completion_view, name='profile_completion'),
    path('profile/', views.profile_view, name='profile'),
    path("finanzas", views.finance, name='finanzas'),
    path("gestion", views.gestion, name='gestion'),
    path("servicios", views.servicios, name='servicios'),
    path("somos", views.somos, name='somos'),

    # Dashboards
    path('cliente/dashboard/', views.cliente_dashboard, name='cliente_dashboard'),
    path('proveedor/dashboard/', views.proveedor_dashboard, name='proveedor_dashboard'),
    path('postulante/dashboard/', views.postulante_dashboard, name='postulante_dashboard'),

    # Productos (Proveedores)
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),

    # Ofertas de Empleo (Clientes)
    path('ofertas/crear/', views.crear_oferta, name='crear_oferta'),
    path('ofertas/<int:pk>/editar/', views.editar_oferta, name='editar_oferta'),
    path('ofertas/<int:pk>/eliminar/', views.eliminar_oferta, name='eliminar_oferta'),

    # Postulantes
    path('ofertas/', views.lista_ofertas, name='lista_ofertas'),
    path('ofertas/<int:pk>/', views.detalle_oferta, name='detalle_oferta'),

    
]
