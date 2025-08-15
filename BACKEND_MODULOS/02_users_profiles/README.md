Módulo 02 - Gestión de Usuarios y Perfiles 👥

Este módulo centraliza todo lo relacionado con usuarios, perfiles, autenticación, verificación y búsqueda, desarrollado en Django con Django REST Framework.

HU01 – Gestión de Usuarios (UserCRUD)

Descripción:
Permite realizar operaciones CRUD sobre usuarios, con validaciones y manejo de errores.

Estructura de Archivos:

views_simple.py → Vistas simplificadas

urls_simple.py → Rutas para el CRUD

backend/HU01_UserCRUD/models/user.py → Modelo principal de usuario

backend/HU01_UserCRUD/views/UserController.py → Lógica de control

Endpoints:

GET /api/crud/ping/ → Estado del módulo

GET /api/crud/test/ → Página de prueba

GET /api/crud/users/ → Listar usuarios

POST /api/crud/users/ → Crear usuario

PUT /api/crud/users/<id>/ → Actualizar usuario

DELETE /api/crud/users/<id>/ → Eliminar usuario

Criterios de Aceptación:

 Un usuario se crea correctamente cuando recibe un 201 Created y contiene todos los campos obligatorios.

 La actualización devuelve 200 OK y refleja los cambios realizados.

 La eliminación devuelve 204 No Content.

 Listar usuarios devuelve un arreglo en formato JSON con al menos un usuario cuando existan registros.

HU02 – Gestión de Perfiles (ProfileManagement)

Descripción:
Administra datos personales, foto de perfil y estado de verificación de cada usuario.

Estructura:

controllers/profile_controller.py → Control de perfiles

controllers/compatibility_controller.py → Lógica de compatibilidad

users/models.py → Modelo de usuario extendido

services/profile_service.py → Lógica de negocio

forms.py → Formularios

serializers.py → Serializadores DRF

Campos:
first_name, last_name, materno, email, phone, genero, is_verified, photo

Endpoints:

GET /api/profile/ping/ → Estado del módulo

GET /api/profile/me/ → Perfil actual

PUT /api/profile/me/ → Actualizar perfil

POST /api/profile/upload-photo/ → Subir foto

Criterios de Aceptación:

 Un usuario autenticado puede obtener su perfil con 200 OK.

 Actualizar datos retorna 200 OK y los campos modificados.

 Subir foto devuelve 201 Created y la nueva URL de imagen.

 Campos como email y phone validan formato correctamente.

HU03 – Cambio de Contraseña (ChangePassword)

Descripción:
Permite cambiar la contraseña y validar la actual antes del cambio.

Estructura:

views_simple.py

urls_simple.py

backend/HU03_ChangePassword/views/ChangePasswordController.py

Endpoints:

GET /api/password/ping/ → Estado

GET /api/password/test/ → Página de prueba

POST /api/password/change-password/ → Cambiar contraseña

POST /api/password/validate-password/ → Validar contraseña actual

Criterios de Aceptación:

 El cambio de contraseña requiere la contraseña actual válida.

 Contraseña nueva cumple reglas (mínimo 8 caracteres, combinación de letras y números).

 El endpoint retorna 200 OK con mensaje de confirmación.

HU04 – Verificación de Email (EmailVerification)

Descripción:
Envía códigos de verificación y valida correos electrónicos de usuarios.

Estructura:

Models/UserVerificationCode.py

Services/email_service.py

Services/verification_service.py

Controllers/VerificationController.py

views.py

urls_simple.py

Endpoints:

GET /api/auth/ping/ → Estado

POST /api/auth/send-verify-email/ → Enviar código

POST /api/auth/verify-email/ → Verificar código

Criterios de Aceptación:

 El envío de código devuelve 200 OK e indica que el correo fue enviado.

 El código tiene una validez configurada (ej. 10 minutos).

 La verificación correcta actualiza is_verified = true.

 Códigos inválidos o expirados devuelven 400 Bad Request.

HU05 – Filtros de Búsqueda (UserSearchFilters)

Descripción:
Implementa búsqueda avanzada y filtrado de usuarios con paginación.

Estructura:

models/profile.py

views/search_controller.py

views/search_html_view.py

requests/search_users_form.py

Endpoints:

GET /api/users/ → Búsqueda con parámetros (search, per_page, filtros adicionales)

Criterios de Aceptación:

 Las búsquedas sin parámetros devuelven un error o lista vacía según configuración.

 La respuesta está paginada y contiene count, next, previous, results.

 Los filtros funcionan correctamente combinados (por ejemplo, género + nombre).

 La búsqueda por texto parcial devuelve coincidencias esperadas.

Interfaz de Usuario

📄 templates/hu02.html → Página central con:

Perfil editable con avatar

Modales para cambio de email (HU04) y contraseña (HU03)

Integración total con las APIs

Diseño responsive

Funcionalidades Clave

Usuarios → CRUD con validaciones.

Perfiles → Foto, datos, verificación.

Seguridad → Cambio y validación de contraseñas.

Verificación → Códigos y actualización de estado.

Búsqueda → Filtros y paginación.
