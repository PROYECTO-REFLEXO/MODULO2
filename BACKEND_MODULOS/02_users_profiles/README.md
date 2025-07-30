# Estructura de 02_users_profiles

Esta carpeta ahora está organizada según las **Historias de Usuario (HU)** principales del módulo de gestión de usuarios y perfiles. Cada subcarpeta corresponde a una funcionalidad clave del sistema, facilitando la identificación y el mantenimiento del código relacionado con cada requerimiento.

## Organización por Historias de Usuario (HU)

- **HU01_UserCRUD/**: Gestión completa de usuarios (alta, baja, modificación, consulta). Incluye controladores, modelos, requests, resources y servicios para el CRUD de usuarios.
- **HU02_ProfileManagement/**: Gestión y edición de perfil de usuario. Incluye controladores, servicios y requests para la edición de datos personales y gestión de imágenes de perfil.
- **HU03_ChangePassword/**: Cambio y recuperación de contraseña. Incluye controladores, servicios y requests para el cambio y recuperación de contraseñas, así como lógica de primer login.
- **HU04_EmailVerification/**: Verificación de email de usuario. Incluye controladores, servicios, requests, mails, modelos y vistas para la verificación de correo electrónico y procesos relacionados.
- **HU05_UserSearchFilters/**: Búsqueda y filtros de usuarios. Incluye requests y servicios para la búsqueda avanzada y filtrado de usuarios.

## Estructura interna de cada HU

Cada HU puede contener las siguientes carpetas según corresponda:

- **Controllers/**: Controladores que gestionan las solicitudes HTTP.
- **Models/**: Modelos de datos.
- **Requests/**: Validaciones de datos de entrada.
- **Resources/**: Transformadores de respuestas API.
- **Services/**: Lógica de negocio y operaciones complejas.
- **Mails/**: Clases para el envío de correos electrónicos (solo HU04).
- **Views/**: Vistas Blade para correos electrónicos y procesos de verificación (solo HU04).

## Ejemplo de estructura

```
02_users_profiles/
  ├── HU01_UserCRUD/
  │   ├── Controllers/
  │   ├── Models/
  │   ├── Requests/
  │   ├── Resources/
  │   └── Services/
  ├── HU02_ProfileManagement/
  │   ├── Controllers/
  │   ├── Requests/
  │   └── Services/
  ├── HU03_ChangePassword/
  │   ├── Controllers/
  │   ├── Requests/
  │   └── Services/
  ├── HU04_EmailVerification/
  │   ├── Controllers/
  │   ├── Requests/
  │   ├── Services/
  │   ├── Mails/
  │   ├── Models/
  │   └── Views/
  └── HU05_UserSearchFilters/
      ├── Requests/
      └── Services/
```

## ¿Qué hace cada archivo?

- **Controllers/**: Gestionan las peticiones y respuestas HTTP.
- **Models/**: Definen la estructura y relaciones de los datos.
- **Requests/**: Validan los datos recibidos en las solicitudes.
- **Resources/**: Transforman los modelos en respuestas API.
- **Services/**: Implementan la lógica de negocio y operaciones complejas.
- **Mails/**: Definen el contenido y destinatarios de los correos de verificación.
- **Views/**: Plantillas visuales para los correos electrónicos enviados a los usuarios.

Esta organización por historias de usuario facilita el mantenimiento, la escalabilidad y la comprensión del código, permitiendo que cada funcionalidad evolucione de forma independiente y ordenada. 