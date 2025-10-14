from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

# Modelo para el catálogo de productos o servicios de un proveedor
class Catalogo(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='catalogo')
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Producto/Servicio")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    imagen = models.ImageField(upload_to='catalogo/productos/', blank=True, null=True, verbose_name="Imagen del Producto")

    def __str__(self):
        return f'{self.nombre} - {self.proveedor.nombre_empresa}'

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

# Modelo para el formulario de contacto
class Contacto(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('respondido', 'Respondido'),
        ('descartado', 'Descartado'),
    ]
    CATEGORIA_CHOICES = [
        ('dueño', 'Dueño de negocio / encargado'),
        ('proveedor', 'Proveedor de servicios o productos'),
        ('gubernamental', 'Entidad gubernamental'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='otro')

    def __str__(self):
        return f'{self.nombre} - {self.email}'

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
