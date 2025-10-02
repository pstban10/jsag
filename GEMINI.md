# Proyecto: JsAsesoriaG

## Descripción General

**JsAsesoriaG** es una aplicación web desarrollada en Django que sirve como plataforma de gestión para una consultora de servicios. La aplicación gestiona tres tipos de perfiles de usuario:

- **Clientes:** Empresas o individuos que contratan los servicios de la consultora.
- **Proveedores:** Empresas o profesionales que ofrecen servicios a la consultora.
- **Postulantes:** Personas que buscan empleo dentro de la consultora o dentro de su catalogo de clientes.

La plataforma permite a los usuarios registrarse, completar su perfil según su tipo y acceder a un panel de control personalizado.

## Tecnologías Utilizadas

- **Backend:** Django
- **Autenticación:** `django-allauth` para el registro de usuarios, inicio de sesión y autenticación social (Google).
- **Base de Datos:** SQLite3 (para desarrollo).
- **Frontend:** Plantillas de Django con HTML, CSS y JavaScript. Se utiliza `crispy-forms` y `crispy-bootstrap5` para la estilización de formularios.
- **Dependencias Adicionales:** `django-environ` para la gestión de variables de entorno.

## Estado Actual del Proyecto

El proyecto ha superado la fase inicial y cuenta con mejoras significativas en la interfaz de usuario, localización y optimización para motores de búsqueda (SEO).

Las funcionalidades implementadas y mejoras realizadas hasta ahora son:

- **Autenticación de Usuarios:** Registro, inicio de sesión y cierre de sesión funcionales. Autenticación con Google configurada.
- **Perfiles de Usuario:**
    - Creación de un perfil base `Profile` al registrar un nuevo usuario.
    - Un flujo de "completar perfil" que solicita al usuario que elija un tipo de perfil (`cliente`, `proveedor` o `postulante`).
    - Formularios específicos para cada tipo de perfil para recopilar información adicional.
- **Vistas y Paneles de Control:**
    - Vistas para el registro, inicio de sesión y completar el perfil.
    - Paneles de control básicos para cada tipo de usuario (`cliente/dashboard.html`, `proveedor/dashboard.html`, `postulante/dashboard.html`).
    - Páginas estáticas como "Quiénes Somos", "Servicios", "Finanzas" y "Gestión".
- **Formulario de Contacto:**
    - Creación de un modelo `Contacto` para almacenar los mensajes recibidos.
    - Implementación de una vista para procesar el formulario y guardar los datos.
    - Visualización de un mensaje de éxito en un modal emergente tras el envío.
    - Acceso a los mensajes para administradores a través del panel de Django.
- **Mejoras de Interfaz y Contenido (UI/UX):**
    - **Localización a Español Argentino:** Se ha adaptado todo el texto de las plantillas para usar el "voseo" y expresiones comunes de Argentina, creando una experiencia más cercana para el usuario local.
    - **Nueva Sección "Nuestro Equipo":** Se ha añadido una sección en la página de inicio para presentar a los miembros del equipo, con un diseño profesional y responsivo.
    - **Reemplazo de Texto de Relleno:** Se eliminó el texto "Lorem Ipsum" de las páginas `banco_cv.html` y `mi_perfil.html`, sustituyéndolo por contenido relevante.
    - **Botones Flotantes y Modal de Video:** Se han añadido botones flotantes para WhatsApp y un video de YouTube. El botón de YouTube abre un modal con un video que se reproduce automáticamente.
    - **Modal "En Construcción":** Se ha creado un modal para la sección "Iniciar Sesión" para comunicar a los usuarios que esta funcionalidad está en desarrollo.
- **Optimización para Motores de Búsqueda (SEO):**
    - Se ha refactorizado la plantilla `base.html` para permitir la inclusión de meta-tags de SEO (título, descripción) de forma dinámica en cada página.
    - Se han añadido títulos y meta descripciones únicos y optimizados a todas las páginas principales y de contenido estático.
    - Se mejoró el texto alternativo (alt text) de las imágenes para mejorar la accesibilidad y el posicionamiento en búsqueda de imágenes.

## Plan de Desarrollo y Próximos Pasos

El objetivo es expandir la funcionalidad de la plataforma para convertirla en una herramienta de gestión completa. A continuación, se detallan los pasos a seguir:

### 1. **Refinamiento de los Perfiles y Paneles de Control**

- **Objetivo:** Mejorar la experiencia del usuario y la funcionalidad de los paneles de control.
- **Tareas:**
    - **Panel de Cliente:**
        - Mostrar los servicios contratados.
        - Permitir la solicitud de nuevos servicios.
        - Visualizar el estado de los proyectos.
    - **Panel de Proveedor:**
        - Mostrar los servicios ofrecidos.
        - Gestionar la disponibilidad y tarifas.
        - Ver las solicitudes de servicios de la consultora.
    - **Panel de Postulante:**
        - Ver las ofertas de empleo disponibles.
        - Postularse a las ofertas.
        - Hacer seguimiento del estado de sus postulaciones.

### 2. **Desarrollo del Módulo de Servicios**

- **Objetivo:** Crear un sistema para gestionar los servicios que ofrece la consultora.
- **Tareas:**
    - Crear un modelo `Servicio` con campos como `nombre`, `descripcion`, `precio`, etc.
    - Desarrollar vistas para que los administradores puedan crear, editar y eliminar servicios.
    - Implementar la lógica para que los clientes puedan contratar servicios.

### 3. **Implementación de un Módulo de Proyectos**

- **Objetivo:** Gestionar los proyectos que la consultora realiza para sus clientes.
- **Tareas:**
    - Crear un modelo `Proyecto` que relacione a un `Cliente` con uno o más `Servicios`.
    - Definir los estados de un proyecto (ej. "Iniciado", "En Progreso", "Finalizado").
    - Desarrollar vistas para que los clientes y administradores puedan ver el estado de los proyectos.

### 4. **Módulo de Ofertas de Empleo y Postulaciones**

- **Objetivo:** Crear un sistema de gestión de recursos humanos para los postulantes.
- **Tareas:**
    - Crear un modelo `OfertaEmpleo` con campos como `titulo`, `descripcion`, `requisitos`, etc.
    - Permitir que los postulantes se postulen a las ofertas.
    - Crear un modelo `Postulacion` para registrar las postulaciones de los usuarios.
    - Desarrollar vistas para que los administradores puedan gestionar las ofertas y las postulaciones.

### 5. **Mejoras en la Interfaz de Usuario y Experiencia de Usuario (UI/UX)**

- **Objetivo:** Modernizar el diseño de la aplicación y mejorar la usabilidad.
- **Tareas:**
    - **Migración a un Frontend Moderno:** Considerar la posibilidad de migrar el frontend a un framework como React o Vue.js para crear una Single Page Application (SPA).
    - **API REST:** Si se decide migrar el frontend, será necesario desarrollar una API REST con Django REST Framework para comunicar el backend con el frontend.
    - **Diseño:** Mejorar el diseño de las plantillas actuales, asegurando que la aplicación sea responsiva y visualmente atractiva.

### 6. **Instrucciones para el Asistente (Gemini)**

- **Comunicación:** La comunicación con el usuario será en español.
- **Planificación:** Antes de realizar cualquier cambio, se debe presentar un plan de acción al usuario.
- **Verificación:** Después de cada cambio importante, se deben verificar las funcionalidades afectadas.
- **Commits:** No se deben realizar commits directamente. Se pueden sugerir mensajes de commit al usuario.
- **Organización:** Mantener la estructura del proyecto y seguir las convenciones de Django.
- **Documentación:** Mantener este archivo `GEMINI.md` actualizado con el progreso del proyecto.