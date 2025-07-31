profile controller
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Mostrar el perfil del usuario autenticado.
        """
        user = request.user
        # Simula UserResource de Laravel
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "photo_url": user.photo_url if hasattr(user, 'photo_url') else None,
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Actualizar el perfil del usuario autenticado.
        """
        user = request.user
        data = request.data

        # Validaciones básicas como harías en UpdateProfileRequest
        if 'email' in data and not data['email']:
            return Response({'error': 'El correo no puede estar vacío'}, status=status.HTTP_400_BAD_REQUEST)

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)

        try:
            user.save()
            return Response({
                "message": "Perfil actualizado correctamente",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "photo_url": user.photo_url if hasattr(user, 'photo_url') else None,
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Error al actualizar perfil", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)