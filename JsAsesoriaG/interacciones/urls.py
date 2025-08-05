
from django.urls import path
from . import views

app_name = 'interacciones'

urlpatterns = [
    path('notificaciones/', views.lista_notificaciones, name='lista_notificaciones'),
    path('chat/', views.vista_chat, name='vista_chat'),
    path('chat/<int:conversacion_id>/mensajes/', views.obtener_mensajes, name='obtener_mensajes'),
    path('chat/<int:conversacion_id>/enviar/', views.enviar_mensaje, name='enviar_mensaje'),
]
