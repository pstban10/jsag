from django.contrib import admin
from .models import Profile, Cliente, Proveedor, Postulante

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'is_profile_complete')
    list_filter = ('user_type', 'is_profile_complete')
    search_fields = ('user__username',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre_negocio', 'cuit')
    search_fields = ('nombre_negocio', 'cuit')

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre_empresa', 'cuit')
    search_fields = ('nombre_empresa', 'cuit')

@admin.register(Postulante)
class PostulanteAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre_completo', 'cuil')
    search_fields = ('nombre_completo', 'cuil')