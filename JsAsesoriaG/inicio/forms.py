from django import forms
from .models import Profile, Cliente, Proveedor, Postulante

class ProfileTypeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_type']
        labels = {
            'user_type': 'Selecciona tu tipo de perfil'
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_negocio', 'cuit', 'direccion', 'foto_perfil']

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre_empresa', 'cuit', 'descripcion', 'foto_perfil']

class PostulanteForm(forms.ModelForm):
    class Meta:
        model = Postulante
        fields = ['nombre_completo', 'cuil', 'presentacion', 'cv', 'foto_perfil']
