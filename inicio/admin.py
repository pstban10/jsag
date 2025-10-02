from django.contrib import admin
from .models import Profile, Cliente, Proveedor, Postulante, Contacto

# Register your models here.
admin.site.register(Profile)
admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(Postulante)
admin.site.register(Contacto)
