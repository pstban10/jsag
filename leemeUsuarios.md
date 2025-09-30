Hola, quiero que actúes como asistente experto en desarrollo de backend Django, con especial foco en diseño de modelos, lógica de usuarios y experiencia administrativa personalizada.
Estoy construyendo una plataforma de asesoramiento gastronómico profesional y necesito implementar un sistema multiusuario con lógica diferenciada por roles.

📌 Información general del proyecto
Plataforma web construida con Django + Bootstrap

Frontend ya avanzado, con foco en consultoría gastronómica

Branding sólido y base de datos ya funcional con autenticación por django-allauth

Objetivo: brindar servicios, productos y oportunidades laborales a negocios gastronómicos

🧑‍💼 Tipos de usuario requeridos:
1. Cliente
Puede:

Ver perfiles de proveedores y postulantes

Publicar ofertas de empleo o solicitudes de servicios/productos

Tener un perfil editable (foto, info del negocio)

Agregar productos a un carrito

Generar una orden de compra como .txt (no incluye pasarela de pago)

2. Proveedor
Puede:

Cargar productos y promociones especiales (descuentos por monto o tipo de pago)

Ver órdenes de compra dirigidas a ellos

Ver solicitudes de productos/servicios

Ver perfiles de postulantes

3. Postulante
Puede:

Cargar CV (.pdf o .docx)

Editar perfil (datos personales, presentación, estudios)

Ver y postularse a ofertas laborales

💬 Funcionalidades compartidas
Dashboard donde todos los tipos de usuario pueden publicar y responder posteos (tipo "tablero de servicios/comunidad")

Comunicación entre usuarios dentro de la plataforma

Administración de perfiles, imágenes y datos personalizados

Generación de órdenes de compra sin pagos, sólo confirmaciones

🎯 Qué necesito de vos (IA generativa):
Analizá la estructura de mi proyecto actual y detectá:

Cambios necesarios en modelos (models.py)

Cambios sugeridos en vistas y formularios (views.py, forms.py)

Uso óptimo del sistema de autenticación con roles

Cómo separar lógica de cliente/proveedor/postulante sin duplicar demasiado código

Proponé un plan paso a paso para:

Crear los modelos y relaciones necesarias

Estructurar la base de datos para escalar

Implementar formularios y validaciones

Organizar las vistas y URLs por tipo de usuario

Integrar todo con el panel administrativo (si es útil)

Dame sugerencias técnicas adicionales, como:

Paquetes recomendados (ej: django-roles, django-guardian, django-polymorphic)

Buenas prácticas para manejar permisos, vistas y dashboards según el tipo de usuario

Ideas para optimizar la experiencia UX/UI en el backend

Notificaciones o alertas internas entre usuarios

Si algo no está claro o te falta información, haceme preguntas puntuales para completar el análisis.

🔚 Output esperado:
🧠 Resumen de acciones necesarias

📋 Lista de tareas ordenadas por prioridad

💡 Recomendaciones específicas (con enlaces a paquetes o prácticas si aplica)

❓ Preguntas clave si algún punto es ambiguo