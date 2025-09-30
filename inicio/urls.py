
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('profile/', views.profile_completion_view, name='profile_completion'),
    path("finanzas", views.finance, name='finanzas'),
    path("gestion", views.gestion, name='gestion'),
    path("servicios", views.servicios, name='servicios'),
    path("somos", views.somos, name='somos'),

    # Dashboards
    path('cliente/dashboard/', views.cliente_dashboard, name='cliente_dashboard'),
    path('proveedor/dashboard/', views.proveedor_dashboard, name='proveedor_dashboard'),
    path('postulante/dashboard/', views.postulante_dashboard, name='postulante_dashboard'),

    # Nuevas páginas
    path('invertir/', views.invertir_view, name='invertir'),
    path('proveedores-vip/', views.proveedores_vip_view, name='proveedores_vip'),
    path('asesoria-legal/', views.asesoria_legal_view, name='asesoria_legal'),
    path('mi-catalogo/', views.mi_catalogo_view, name='mi_catalogo'),
    path('banco-cv/', views.banco_cv_view, name='banco_cv'),
    path('mi-perfil/', views.mi_perfil_view, name='mi_perfil'),

    # Catálogo
    path('mi-catalogo/agregar/', views.agregar_producto_view, name='agregar_producto'),
    path('mi-catalogo/editar/<int:pk>/', views.editar_producto_view, name='editar_producto'),
    path('mi-catalogo/eliminar/<int:pk>/', views.eliminar_producto_view, name='eliminar_producto'),
]
