from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from your_app.serializers.user_serializer import UserSerializer

User = get_user_model()

class ProfileService:
    @staticmethod
    def get_authenticated_user(request):
        """
        Obtiene el perfil del usuario autenticado con sus relaciones.
        """
        user = request.user
        # Cargar relaciones (asumiendo ForeignKey)
        user = User.objects.select_related(
            'region', 'province', 'district', 'document_type', 'country'
        ).get(pk=user.pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def update_authenticated_user(request, data):
        """
        Actualiza datos del usuario autenticado.
        """
        user = request.user
        # Manejar password si se incluye
        if 'password' in data:
            data['password'] = make_password(data['password'])
        # Actualizar campos permitidos
        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Volver a cargar relaciones y serializar
        user = User.objects.select_related(
            'region', 'province', 'district', 'document_type', 'country'
        ).get(pk=user.pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
