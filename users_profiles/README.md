# Módulo 02_users_profiles

## Descripción

Este módulo proporciona una gestión completa de perfiles de usuario, incluyendo:

- **Gestión de Usuarios**: Creación, actualización y administración de usuarios
- **Perfiles de Usuario**: Información personal detallada con campos editables
- **Gestión de Contraseñas**: Cambio seguro de contraseñas con verificación
- **Verificación de Email**: Sistema de códigos de verificación para cambios de email
- **Fotos de Perfil**: Gestión de imágenes de perfil de usuario

## Estructura del Módulo

```
config/
manage.py
02_users_profiles/
├── __init__.py
├── apps.py
├── models/
│   ├── __init__.py
│   ├── user.py           # Modelo User personalizado
│   ├── profile.py        # Modelo UserProfile
│   └── verification.py   # Modelo UserVerificationCode
├── serializers/
│   ├── __init__.py
│   ├── user.py           # Serializers para User
│   ├── profile.py        # Serializers para UserProfile
│   ├── password.py       # Serializers para gestión de contraseñas
│   └── verification.py   # Serializers para verificación
├── views/
│   ├── __init__.py
│   ├── user.py           # Vistas para gestión de usuarios
│   ├── profile.py        # Vistas para gestión de perfiles
│   ├── password.py       # Vistas para gestión de contraseñas
│   └── verification.py   # Vistas para verificación
├── services/
│   ├── __init__.py
│   ├── user_service.py   # Lógica de negocio para usuarios
│   ├── profile_service.py # Lógica de negocio para perfiles
│   ├── password_service.py # Lógica de negocio para contraseñas
│   └── verification_service.py # Lógica de negocio para verificación
├── urls.py               # Configuración de URLs del módulo
├── admin.py              # Configuración del admin de Django
└── tests/                # Tests del módulo
    ├── __init__.py
    └── test_models.py
```

## Características Principales

### 1. Gestión de Usuarios
- Modelo User personalizado que extiende AbstractUser
- Campos adicionales: foto de perfil, teléfono, fecha de nacimiento, ubicación
- Validaciones personalizadas para datos de usuario

### 2. Perfiles de Usuario
- Información personal detallada (nombre, apellidos, género)
- Configuraciones de privacidad (perfil público/privado)
- Cálculo automático de completitud del perfil
- Campos editables según especificaciones del usuario

### 3. Gestión de Contraseñas
- Cambio de contraseña con verificación de contraseña actual
- Restablecimiento de contraseña por email
- Validación de fortaleza de contraseñas
- Historial de cambios de contraseña

### 4. Verificación de Email
- Códigos de verificación de 6 dígitos
- Verificación para cambio de email
- Verificación para cambio de contraseña
- Expiración automática de códigos (15 minutos)
- Límite de intentos de uso

### 5. Fotos de Perfil
- Subida y gestión de imágenes de perfil
- Eliminación de fotos anteriores automáticamente
- Validación de tipos de archivo

## Endpoints de la API

### Usuarios
- `GET /api/users_profiles/user/` - Obtener información del usuario
- `PUT /api/users_profiles/user/update/` - Actualizar información del usuario
- `POST /api/users_profiles/user/photo/` - Subir foto de perfil
- `DELETE /api/users_profiles/user/photo/` - Eliminar foto de perfil
- `GET /api/users_profiles/user/search/` - Buscar usuarios
- `GET /api/users_profiles/user/<username>/` - Perfil público de usuario

### Perfiles
- `GET /api/users_profiles/profile/` - Obtener perfil del usuario
- `POST /api/users_profiles/profile/create/` - Crear perfil
- `PUT /api/users_profiles/profile/update/` - Actualizar perfil
- `PUT /api/users_profiles/profile/settings/` - Configuraciones del perfil
- `GET /api/users_profiles/profile/completion/` - Completitud del perfil
- `GET /api/users_profiles/profile/search/` - Buscar perfiles públicos
- `GET /api/users_profiles/profile/<username>/` - Perfil público

### Contraseñas
- `POST /api/users_profiles/password/change/` - Cambiar contraseña
- `POST /api/users_profiles/password/reset/` - Solicitar restablecimiento
- `POST /api/users_profiles/password/reset/confirm/` - Confirmar restablecimiento
- `POST /api/users_profiles/password/strength/` - Validar fortaleza
- `GET /api/users_profiles/password/history/` - Historial de cambios
- `GET /api/users_profiles/password/policy/` - Política de contraseñas

### Verificación
- `POST /api/users_profiles/verification/code/` - Solicitar código
- `POST /api/users_profiles/verification/email/change/` - Cambiar email
- `POST /api/users_profiles/verification/email/change/confirm/` - Confirmar cambio
- `POST /api/users_profiles/verification/code/resend/` - Reenviar código
- `GET /api/users_profiles/verification/status/` - Estado de verificación
- `POST /api/users_profiles/verification/email/` - Verificar email
- `POST /api/users_profiles/verification/email/confirm/` - Confirmar verificación

## Instalación y Configuración

### 1. Agregar a INSTALLED_APPS
```python
INSTALLED_APPS = [
    # ... otras apps
    '02_users_profiles',
]
```

### 2. Configurar AUTH_USER_MODEL
```python
AUTH_USER_MODEL = '02_users_profiles.User'
```

### 3. Incluir URLs en el proyecto principal
```python
# urls.py del proyecto
from django.urls import path, include

urlpatterns = [
    # ... otras URLs
    path('api/users_profiles/', include('02_users_profiles.urls')),
]
```

### 4. Configurar archivos multimedia
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 5. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

## Uso

### Crear un usuario
```python
from 02_users_profiles.services.user_service import UserService

user_data = {
    'username': 'usuario1',
    'email': 'usuario1@example.com',
    'password': 'Contraseña123!',
    'first_name': 'Juan',
    'last_name': 'Pérez'
}

user = UserService.create_user(user_data)
```

### Actualizar perfil
```python
from 02_users_profiles.services.profile_service import ProfileService

profile_data = {
    'first_name': 'Juan Carlos',
    'paternal_lastname': 'Pérez',
    'maternal_lastname': 'García',
    'gender': 'M',
    'email': 'juan@example.com'
}

ProfileService.update_profile(user, profile_data)
```

### Solicitar código de verificación
```python
from 02_users_profiles.models import UserVerificationCode

verification_code = UserVerificationCode.create_code(
    user=user,
    verification_type='email_change',
    target_email='nuevo@example.com'
)
```

## Personalización

### Campos del perfil
Los campos del perfil se pueden personalizar editando el modelo `UserProfile` en `models/profile.py`.

### Validaciones
Las validaciones se pueden personalizar en los serializers correspondientes.

### Configuraciones
Las configuraciones del módulo se pueden modificar en `settings.py` del proyecto.

## Tests

El módulo incluye una suite de tests con pytest ya configurada para ejecutarse dentro de `02_users_profiles/` usando `pytest.ini` y settings de prueba internos.

### Ejecutar tests (recomendado)

1) Instalar dependencias
```bash
pip install -r requirements.txt
```

2) Ejecutar tests del módulo

PowerShell (Windows):
```bash
cd .\02_users_profiles
cle
```

Bash (Linux/Mac):
```bash
cd 02_users_profiles
pytest -c pytest.ini -q
```

3) Opcional: ejecutar un archivo o selección
```bash
# Un archivo específico
pytest -c pytest.ini tests/test_models.py -q

# Usando -k para filtrar
pytest -c pytest.ini -k models -q
```

4) Opcional: cobertura rápida en consola
```bash
pytest -c pytest.ini --cov=. --cov-report=term-missing -q
```

Notas:
- Los tests usan un `AUTH_USER_MODEL` por defecto (de Django) para simplificar la ejecución.
- No es necesario registrar la app en `INSTALLED_APPS` para correr estos tests.

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte técnico o preguntas, por favor contacta al equipo de desarrollo o abre un issue en el repositorio.
