
# MÓDULO 02 - users_profiles — Instrucciones estrictas para completar y probar

> **Objetivo**: Implementar estrictamente el módulo `users_profiles` conforme a la estructura y a las pruebas incluidas. El repositorio contiene la base del proyecto Django pero muchos archivos están incompletos o contienen marcadores/errores. Este README explica **qué** hay que implementar, **dónde** y **cómo** comprobar que está hecho correctamente.

---

## Resumen del proyecto
- Proyecto Django mínimo con app `users_profiles`.
- `AUTH_USER_MODEL` ya apunta a `users_profiles.User` (revisar `config/settings.py`).
- Base de datos por defecto: SQLite (`db.sqlite3`).
- Dependencias en `requirements.txt`.

---

## Requisitos previos
- Python 3.10+ (se recomiendan 3.11/3.12).
- Virtualenv / venv.
- Recomendado: sistema UNIX-like o WSL si trabajas en Windows.

---

## Instalación (pasos exactos)

1. Clona / coloca el proyecto y entra en la carpeta del repo (el zip ya está descomprimido aquí):
   ```bash
   cd /path/to/MODULO2-main
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # macOS / Linux
   .venv\Scripts\activate       # Windows (PowerShell)
   ```

3. Instala dependencias:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Archivos importantes:
   - `config/settings.py` — configuración del proyecto (AUTH_USER_MODEL ya definido).
   - `users_profiles/` — todo el trabajo a implementar (models, serializers, views, services, tests).
   - `structure_02.txt` — estructura y nombres sugeridos de archivos (usarla como referencia).

---

## Configuración adicional (obligatoria antes de correr)
- Crear carpetas para media (fotos de perfil):
  ```bash
  mkdir media
  mkdir media/profile_photos
  ```
- Revisar `config/settings.py` y confirmar:
  - `AUTH_USER_MODEL = 'users_profiles.User'` (ya presente).
  - `EMAIL_BACKEND` está en modo consola (desarrollo) — está OK para pruebas.
- Si usas `python-decouple` y `.env`, crea `.env` con `SECRET_KEY` y `DEBUG=True`. (No obligatorio: el proyecto tiene valores por defecto).

---

## Migraciones y servidor
1. Crear migraciones (si implementas/añades modelos nuevos):
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. (Opcional) Crear superuser para pruebas manuales:
   ```bash
   python manage.py createsuperuser
   ```

3. Levantar servidor:
   ```bash
   python manage.py runserver
   ```

---

## Cómo ejecutar los tests (estrictamente)
Se usa pytest. Desde la raíz del proyecto (`MODULO2-main`):

```bash
# correr todos los tests
pytest -q

# o con reporte de cobertura (si instalaste coverage)
pytest --maxfail=1 --disable-warnings -q
```

El objetivo final es **hacer que `pytest` pase sin errores** en el subdirectorio `users_profiles/tests`.

---

## Qué hay que implementar (lista estricta por archivo)

### 1. `users_profiles/models/`
- `user.py`
  - Asegurarse de que la clase `User(AbstractUser)` tiene:
    - Campos opcionales: `profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)`
    - Métodos:
      - `def full_name(self):` → devuelve `"first_name last_name"` o `username` si faltan.
      - `def has_profile_photo(self):` → `bool(self.profile_photo)`
      - `def get_profile_photo_url(self):` → devuelve `self.profile_photo.url` o `None`.
- `profile.py`
  - `UserProfile` con campos básicos (bio, birth_date, gender, location, phone, etc.) si no existen.
  - `def completion_percentage(self)` que toma una lista de campos (defínela en el método/docstring) y devuelve un entero 0-100.
- `verification.py`
  - Revisar que `UserVerificationCode` tenga métodos:
    - `create_code(cls, user, verification_type, target_email=None)` -> crea y retorna instancia.
    - `verify_code(cls, user, code, verification_type)` -> verifica validez, controla intentos y expiración.
    - `is_expired(self)` -> True/False
    - `can_attempt(self)` -> True/False (limita intentos).
  - Ya existe lógica en el archivo — revisa que esté correcta y haz ajustes si `tests` fallan.

### 2. `users_profiles/serializers/`
- `user.py`:
  - `UserSerializer` (lectura): debe exponer `id, username, email, first_name, last_name, full_name, profile_photo_url, is_active` y otros que se consideren necesarios.
  - `UserCreateSerializer` o `UserRegisterSerializer`: incluir `password` y `password_confirm`. Validar `password_confirm == password` y `validate_password`.
  - `UserUpdateSerializer`: permitir actualizar campos no sensibles (no el password).
  - `UserProfilePhotoSerializer`: `ImageField` para `profile_photo`. `update()` debe:
    - Borrar archivo anterior si existe (`instance.profile_photo.delete(save=False)`).
    - Asignar la nueva imagen y guardar la instancia.
- `password.py`:
  - `PasswordChangeSerializer`: validar `current_password` usando `authenticate` o `user.check_password`, y usar `validate_password` para `new_password`.
  - Otros serializers de restablecimiento si existen: implementarlos según las pruebas o comentarios.

- `verification.py`:
  - Serializers para solicitar/confirmar códigos (campo `code` de 6 dígitos), validar formato (`isdigit()` y longitud 6), y manejar `verification_type`.

**Importante**: corregir errores obvios de sintaxis en los archivos (`Fals`, `raise s`, `...`).

### 3. `users_profiles/views/`
Implementar vistas basadas en `generics` o `APIView` que estén listadas en `urls.py`. Para cada vista, confirmar método HTTP y permisos:

- `UserDetailView` — `GET` → retorna datos del usuario autenticado; permiso `IsAuthenticated`.
- `UserUpdateView` — `PUT/PATCH` → actualizar usuario (autenticado).
- `UserProfilePhotoView` — `PUT/PATCH` → actualizar foto (autenticado) y usar `UserProfilePhotoSerializer`.
- `UserSearchView` — `GET` → búsqueda por username/email (puede ser público o autenticado según tests).
- `Profile*` views — CRUD para `UserProfile`.
- Vistas de `Password`:
  - `PasswordChangeView` — `POST` con `current_password` y `new_password`.
  - Otros endpoints de reset/confirm según `urls.py`.
- Vistas de verificación (`VerificationCodeView`, `EmailChangeView`, `EmailChangeConfirmView`, etc.):
  - Deben integrar `UserVerificationCode.create_code(...)`, enviar email por consola (EMAIL_BACKEND = console), y `verify_code` para confirmar.
  - `VerificationCodeResendView` debe permitir volver a generar código si no ha expirado o según lógica permitida.
  - `VerificationStatusView` devuelve si hay códigos válidos y si el email está verificado.

**Permisos**: cuando aplique, usar `permissions.IsAuthenticated`. Las vistas de creación de usuarios y envío de códigos pueden ser públicas.

### 4. `users_profiles/services/`
- Implementar lógica de negocios separada si el código la requiere (ej.: `user_service.create_user`, `verification_service.send_code_email`, `profile_service.update_profile`). Mantener las firmas usadas por las vistas/serializers y tests.

### 5. `users_profiles/urls.py`
- Ya existe una lista amplia de rutas. Asegúrate de que las vistas referenciadas están implementadas con los nombres importados. Si no las implementas exactamente con esos nombres, actualiza `urls.py` o las vistas para que concuerden.

---

## Endpoints esperados (según `urls.py`)
> Repite exactamente los paths que están en `users_profiles/urls.py`. Implementa y prueba al menos:
- `/api/users/` (router si aplica)
- `/api/users/me/` → GET detalles usuario autenticado
- `/api/users/me/update/` → PUT/PATCH
- `/api/users/me/photo/` → PUT/PATCH con `profile_photo`
- `/api/profile/` → CRUD perfil
- `/api/password/change/` → POST
- `/api/verification/code/` → POST (solicitar)
- `/api/verification/email/change/` → POST
- `/api/verification/email/change/confirm/` → POST (confirmar con código)
- ...y demás rutas listadas en `urls.py`

---

## Validaciones y reglas estrictas (ten en cuenta)
- Los códigos de verificación deben ser numéricos de 6 dígitos.
- Los intentos de verificación deben ser limitados (ej.: max 5 intentos fallidos).
- Los códigos expiran (p. ej. 15 minutos). Hay funciones en `models/verification.py` que ya implementan lógica; úsala o adáptala.
- Validar contraseña con `validate_password` de Django.
- Borrar archivo de imagen anterior al subir nueva foto para evitar acumulación de ficheros.
- Usar `create_user` para crear usuarios (que maneje password hashing).

---

## Comprobaciones rápidas (antes de entregar)
- `python manage.py runserver` arranca sin errores de importación.
- `pytest -q` no muestra errores (todos los tests pasan).
- Prueba manual con `curl` o `httpie`:
  - Crear usuario, loguear (obtener token si usas JWT o sesión), acceder a `/api/users/me/`.
  - Subir `profile_photo` vía multipart/form-data a `/api/users/me/photo/`.
  - Solicitar código de verificación y confirmar (revisar consola donde Django imprime el email).

Ejemplo de `curl` para subir foto (suponiendo token de autenticación):
```bash
curl -X PATCH -H "Authorization: Token <TOKEN>" -F "profile_photo=@/ruta/a/foto.jpg" http://localhost:8000/api/users/me/photo/
```

---

## Checklist final (marca al completar)
- [ ] Corregir errores de sintaxis en todos los archivos `.py`.
- [ ] Implementar las clases/serializers/métodos listados en "Qué hay que implementar".
- [ ] Asegurar coincidencia entre `urls.py` y vistas implementadas.
- [ ] Ejecutar migraciones sin errores.
- [ ] Ejecutar `pytest` y conseguir `OK` en todos los tests.
- [ ] Verificar flujo de verificación por email (se imprime en consola).

---


