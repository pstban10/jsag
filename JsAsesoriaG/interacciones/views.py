from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notificacion, Conversacion, Mensaje
from .forms import MensajeForm

@login_required
def lista_notificaciones(request):
    notificaciones = Notificacion.objects.filter(destinatario=request.user)
    # Marcar todas las notificaciones como leídas al visitar la página
    notificaciones.update(leida=True)
    return render(request, 'interacciones/notificaciones.html', {'notificaciones': notificaciones})

@login_required
def vista_chat(request):
    conversaciones = Conversacion.objects.filter(participantes=request.user)
    return render(request, 'interacciones/chat.html', {'conversaciones': conversaciones})

@login_required
def obtener_mensajes(request, conversacion_id):
    conversacion = get_object_or_404(Conversacion, id=conversacion_id, participantes=request.user)
    mensajes = conversacion.mensajes.all().order_by('fecha_envio')
    # Marcar mensajes como leídos
    mensajes.filter(leido=False).exclude(remitente=request.user).update(leido=True)
    
    data = {
        'mensajes': [
            {
                'remitente': m.remitente.username,
                'contenido': m.contenido,
                'fecha_envio': m.fecha_envio.strftime("%d/%m/%Y %H:%M"),
                'is_self': m.remitente == request.user
            } for m in mensajes
        ]
    }
    return JsonResponse(data)

@login_required
def enviar_mensaje(request, conversacion_id):
    if request.method == 'POST':
        conversacion = get_object_or_404(Conversacion, id=conversacion_id, participantes=request.user)
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.conversacion = conversacion
            mensaje.remitente = request.user
            mensaje.save()
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)