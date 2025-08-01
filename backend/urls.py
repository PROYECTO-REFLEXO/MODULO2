from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('', lambda request: HttpResponse("Bienvenido a la API 👋")),
    path('admin/', admin.site.urls),

    # HU05 - Búsqueda de usuarios
    path('api/users/', include('HU05_UserSearchFilters.urls')),

    # ✅ HU02 - Gestión de perfil
    path('api/profile/', include('HU02_ProfileManagement.urls')),
]
