from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from .models import Profile, Cliente, Proveedor, Postulante, OfertaEmpleo, Postulacion, Notificacion

# Create your tests here.

class BaseTestCase(TestCase):
    """
    Clase base con configuraciones comunes para los tests.
    Crea usuarios de diferentes roles para ser usados en las pruebas.
    """
    def setUp(self):
        # Usuario Cliente
        self.cliente_user = User.objects.create_user(username='testcliente', password='password123')
        self.cliente_user.profile.user_type = 'cliente'
        self.cliente_user.profile.is_profile_complete = True
        self.cliente_user.profile.save()
        self.cliente = Cliente.objects.create(user=self.cliente_user, nombre_negocio='Restaurante Test', cuit='30-12345678-9')

        # Usuario Proveedor
        self.proveedor_user = User.objects.create_user(username='testproveedor', password='password123')
        self.proveedor_user.profile.user_type = 'proveedor'
        self.proveedor_user.profile.is_profile_complete = True
        self.proveedor_user.profile.save()
        self.proveedor = Proveedor.objects.create(user=self.proveedor_user, nombre_empresa='Proveedor Test', cuit='30-87654321-9')

        # Usuario Postulante
        self.postulante_user = User.objects.create_user(username='testpostulante', password='password123')
        self.postulante_user.profile.user_type = 'postulante'
        self.postulante_user.profile.is_profile_complete = True
        self.postulante_user.profile.save()
        self.postulante = Postulante.objects.create(user=self.postulante_user, nombre_completo='Juan Perez', cuil='20-98765432-1')


class TestSignalAndModelCreation(BaseTestCase):
    """Tests para la creación automática de modelos mediante señales."""

    def test_profile_created_for_new_user(self):
        """Verifica que se crea un Profile al crear un User."""
        user = User.objects.create_user(username='newuser', password='password123')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, Profile)

    def test_notification_created_on_postulacion(self):
        """Verifica que se crea una Notificacion para el Cliente al recibir una Postulacion."""
        self.client.login(username='testpostulante', password='password123')
        
        oferta = OfertaEmpleo.objects.create(cliente=self.cliente, titulo='Cocinero', descripcion='...', requisitos='...')
        
        # Contamos las notificaciones ANTES de la postulación
        notificaciones_antes = Notificacion.objects.filter(destinatario=self.cliente_user).count()
        
        # El postulante se postula
        Postulacion.objects.create(oferta=oferta, postulante=self.postulante)
        
        # Contamos las notificaciones DESPUÉS
        notificaciones_despues = Notificacion.objects.filter(destinatario=self.cliente_user).count()
        
        self.assertEqual(notificaciones_despues, notificaciones_antes + 1)
        notificacion = Notificacion.objects.latest('fecha_creacion')
        self.assertEqual(notificacion.destinatario, self.cliente_user)
        self.assertIn('Nueva postulación', notificacion.mensaje)


class TestViewPermissions(BaseTestCase):
    """Tests para asegurar que los roles de usuario tengan los permisos correctos."""

    def test_cliente_can_access_crear_oferta(self):
        """Un Cliente DEBE poder acceder a la página de crear oferta."""
        self.client.login(username='testcliente', password='password123')
        response = self.client.get(reverse('crear_oferta'))
        self.assertEqual(response.status_code, 200)

    def test_postulante_cannot_access_crear_oferta(self):
        """Un Postulante NO DEBE poder acceder a la página de crear oferta."""
        self.client.login(username='testpostulante', password='password123')
        response = self.client.get(reverse('crear_oferta'))
        self.assertEqual(response.status_code, 302) # 302 es el código para redirección
        self.assertRedirects(response, reverse('index'))

    def test_unauthenticated_user_is_redirected(self):
        """Un usuario no logueado debe ser redirigido al login."""
        response = self.client.get(reverse('crear_oferta'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('account_login'), response.url)


class TestClienteFunctionality(BaseTestCase):
    """Tests para las funcionalidades del Cliente (CRUD de Ofertas)."""

    def test_crear_oferta_empleo(self):
        """Prueba la creación de una oferta de empleo."""
        self.client.login(username='testcliente', password='password123')
        ofertas_count_before = OfertaEmpleo.objects.count()
        
        response = self.client.post(reverse('crear_oferta'), {
            'titulo': 'Mozo con experiencia',
            'descripcion': 'Se busca mozo para turno noche.',
            'requisitos': '2 años de experiencia.',
            'tipo_contrato': 'Full-time',
            'activa': True
        })
        
        self.assertEqual(OfertaEmpleo.objects.count(), ofertas_count_before + 1)
        self.assertEqual(response.status_code, 302) # Redirección al dashboard
        self.assertRedirects(response, reverse('cliente_dashboard'))
        
        # Verificamos que la oferta se creó correctamente
        nueva_oferta = OfertaEmpleo.objects.latest('fecha_publicacion')
        self.assertEqual(nueva_oferta.titulo, 'Mozo con experiencia')
        self.assertEqual(nueva_oferta.cliente, self.cliente)