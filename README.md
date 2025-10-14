> Genial, necesito ahora trabajar en otra cosa, en esta pagina web necesito tener administradosres qu podran visualizar los mensajes que nos dejan los interesados en el servicio. estos administradores tendran 
  permisos de staf y necesitan su propio dashboard, en esta dashboard se deberan mostrar los registros de la base de datos de mensajes en forma de tarjetas, y tendran que tener 3 estados -- no leido -- leido -- 
  resuelto, depende de como lo marque un miembro del staff, todos los staff deben poder ver el mismo dashboard

✦ ¡Excelente! Una nueva funcionalidad muy importante. Entendido, necesitas un dashboard para administradores (staff) donde puedan gestionar los mensajes de contacto, visualizarlos como tarjetas y cambiar su estado
  entre "No leído", "Leído" y "Resuelto".

  Este es un plan de acción completo para implementarlo:

   1. Actualizar el Modelo `Contacto`: Primero, modificaré el modelo Contacto en inicio/models.py. Cambiaré los ESTADO_CHOICES actuales (pendiente, respondido, descartado) por los que solicitaste: no_leido, leido, y
      resuelto. Esto requerirá una nueva migración de la base de datos.

   2. Crear el Dashboard de Administrador:
       * Crearé una nueva vista en inicio/views.py que solo será accesible para usuarios marcados como "staff".
       * Esta vista recuperará todos los mensajes de contacto de la base de datos.
       * Crearé una nueva plantilla HTML (admin/dashboard.html) para mostrar estos mensajes.

   3. Diseñar las Tarjetas de Mensaje: En la nueva plantilla, cada mensaje se mostrará como una tarjeta de Bootstrap. El diseño de la tarjeta (por ejemplo, su color de borde) cambiará según su estado para una fácil
      identificación.

   4. Implementar el Cambio de Estado:
       * Cada tarjeta tendrá botones o un menú desplegable para que los administradores puedan cambiar el estado del mensaje (ej: Marcar como leído, Marcar como resuelto).
       * Crearé una vista auxiliar que se encargará de recibir la petición de cambio de estado, actualizar el mensaje en la base de datos y redirigir de nuevo al dashboard.

   5. Crear las Rutas (URLs): Añadiré las nuevas URLs en inicio/urls.py para el dashboard y para la función de cambio de estado.

   6. Añadir Acceso en el Menú: Finalmente, agregaré un enlace al nuevo dashboard en el menú de navegación, que solo será visible para los usuarios que sean staff.

  Es un desarrollo en varias etapas. Si estás de acuerdo, comenzaré con el primer y más fundamental paso: actualizar el modelo `Contacto` y aplicar las migraciones.

  ¿Procedo?

> si, procede

✦ Perfecto. Comenzaré por modificar el modelo Contacto en inicio/models.py para actualizar los estados. Primero, leo el archivo.
 ╭───────────────────────────────╮
 │ ✓  ReadFile inicio\models.py  │
 ╰───────────────────────────────╯
✦ Ok, he leído el archivo. Ahora voy a reemplazar los ESTADO_CHOICES y el valor default en el modelo Contacto.