# Configuración específica del módulo 02_users_profiles

# Configuración de archivos multimedia
PROFILE_PHOTO_UPLOAD_PATH = 'profile_photos/'
MAX_PROFILE_PHOTO_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_PROFILE_PHOTO_FORMATS = ['image/jpeg', 'image/png', 'image/gif']

# Configuración de verificación
VERIFICATION_CODE_LENGTH = 6
VERIFICATION_CODE_EXPIRY_MINUTES = 15
VERIFICATION_MAX_ATTEMPTS = 3

# Configuración de contraseñas
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_NUMBERS = True
PASSWORD_REQUIRE_SPECIAL_CHARS = True

# Configuración de perfiles
PROFILE_COMPLETION_REQUIRED_FIELDS = [
    'first_name', 'paternal_lastname', 'gender', 'email'
]

# Configuración de búsqueda
USER_SEARCH_MAX_RESULTS = 50
PROFILE_SEARCH_MAX_RESULTS = 50

# Configuración de paginación
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Configuración de cache
PROFILE_CACHE_TIMEOUT = 300  # 5 minutos
USER_CACHE_TIMEOUT = 600     # 10 minutos

# Configuración de notificaciones
SEND_EMAIL_VERIFICATION = True
SEND_PASSWORD_RESET_EMAIL = True
SEND_EMAIL_CHANGE_VERIFICATION = True

# Configuración de seguridad
REQUIRE_EMAIL_VERIFICATION = False  # Cambiar a True en producción
REQUIRE_PHONE_VERIFICATION = False
ENABLE_TWO_FACTOR_AUTH = False

# Configuración de logs
LOG_USER_ACTIONS = True
LOG_PROFILE_CHANGES = True
LOG_PASSWORD_CHANGES = True
LOG_VERIFICATION_ATTEMPTS = True
