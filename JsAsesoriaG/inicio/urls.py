
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
]
