from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Perfil base que todos los usuarios tendrán
class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('cliente', 'Cliente'),
        ('proveedor', 'Proveedor'),
        ('postulante', 'Postulante'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, verbose_name="Tipo de Usuario", null=True, blank=True)
    is_profile_complete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.get_user_type_display() or "Sin tipo"}'

# Perfil específico para Clientes
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nombre_negocio = models.CharField(max_length=255, verbose_name="Nombre del Negocio")
    cuit = models.CharField(max_length=13, verbose_name="CUIT")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    foto_perfil = models.ImageField(upload_to='clientes/fotos/', blank=True, null=True, verbose_name="Foto de Perfil")

    def __str__(self):
        return self.nombre_negocio

# Perfil específico para Proveedores
class Proveedor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nombre_empresa = models.CharField(max_length=255, verbose_name="Nombre de la Empresa")
    cuit = models.CharField(max_length=13, verbose_name="CUIT")
    descripcion = models.TextField(verbose_name="Descripción de la Empresa")
    foto_perfil = models.ImageField(upload_to='proveedores/fotos/', blank=True, null=True, verbose_name="Foto de Perfil")

    def __str__(self):
        return self.nombre_empresa

# Perfil específico para Postulantes
class Postulante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nombre_completo = models.CharField(max_length=255, verbose_name="Nombre Completo")
    cuil = models.CharField(max_length=13, verbose_name="CUIL")
    presentacion = models.TextField(verbose_name="Presentación Personal")
    cv = models.FileField(upload_to='postulantes/cvs/', blank=True, null=True, verbose_name="Currículum Vitae (.pdf o .docx)")
    foto_perfil = models.ImageField(upload_to='postulantes/fotos/', blank=True, null=True, verbose_name="Foto de Perfil")

    def __str__(self):
        return self.nombre_completo

class Producto(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Producto")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    imagen = models.ImageField(upload_to='productos/imagenes/', blank=True, null=True, verbose_name="Imagen del Producto")

    def __str__(self):
        return self.nombre

class OfertaEmpleo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ofertas_empleo')
    titulo = models.CharField(max_length=255, verbose_name="Título de la Oferta")
    descripcion = models.TextField(verbose_name="Descripción del Puesto")
    requisitos = models.TextField(verbose_name="Requisitos")
    tipo_contrato = models.CharField(max_length=50, verbose_name="Tipo de Contrato")
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class Postulacion(models.Model):
    oferta = models.ForeignKey(OfertaEmpleo, on_delete=models.CASCADE, related_name='postulaciones')
    postulante = models.ForeignKey(Postulante, on_delete=models.CASCADE, related_name='postulaciones')
    fecha_postulacion = models.DateTimeField(default=timezone.now)
    mensaje = models.TextField(blank=True, null=True, verbose_name="Mensaje Adicional")

    class Meta:
        unique_together = ('oferta', 'postulante') # Evita que un postulante se postule dos veces a la misma oferta

    def __str__(self):
        return f'{self.postulante.nombre_completo} se postuló a {self.oferta.titulo}'

# Señales para crear/actualizar perfiles
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)


