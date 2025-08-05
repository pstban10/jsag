from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('postulacion', 'Postulación'),
        ('mensaje', 'Mensaje'),
        ('general', 'General'),
    ]
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='general')
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    # Enlace genérico a un objeto, por ejemplo, una postulación o una conversación.
    # Esto nos da flexibilidad para notificar sobre diferentes cosas.
    related_object_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Notificación para {self.destinatario.username}: {self.mensaje}"

    class Meta:
        ordering = ['-fecha_creacion']

class Conversacion(models.Model):
    participantes = models.ManyToManyField(User, related_name='conversaciones')
    # Podríamos mantener un enlace a la postulación si todas las conversaciones se originan de una.
    # Si no, podríamos tener un campo de "asunto" o simplemente basarnos en los participantes.
    postulacion = models.ForeignKey('inicio.Postulacion', on_delete=models.CASCADE, related_name='conversaciones', null=True, blank=True)

    def __str__(self):
        return f"Conversación entre {', '.join([p.username for p in self.participantes.all()])}"

class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados')
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(default=timezone.now)
    leido = models.BooleanField(default=False)

    def __str__(self):
        return f"Mensaje de {self.remitente} en {self.conversacion}"

    class Meta:
        ordering = ['fecha_envio']

# --- Señales --- #

@receiver(post_save, sender='inicio.Postulacion')
def crear_notificacion_postulacion(sender, instance, created, **kwargs):
    if created:
        cliente_user = instance.oferta.cliente.user
        mensaje = f"Nueva postulación de {instance.postulante.nombre_completo} para la oferta '{instance.oferta.titulo}'."
        Notificacion.objects.create(
            destinatario=cliente_user,
            tipo='postulacion',
            mensaje=mensaje,
            related_object_id=instance.id
        )

@receiver(post_save, sender=Mensaje)
def crear_notificacion_mensaje(sender, instance, created, **kwargs):
    if created:
        for participante in instance.conversacion.participantes.all():
            if participante != instance.remitente:
                mensaje = f"Nuevo mensaje de {instance.remitente.username}."
                Notificacion.objects.create(
                    destinatario=participante,
                    tipo='mensaje',
                    mensaje=mensaje,
                    related_object_id=instance.conversacion.id
                )