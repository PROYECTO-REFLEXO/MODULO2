from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model

from your_app.serializers.update_profile_serializer import UpdateProfileSerializer
from your_app.services.profile_service import ProfileService

User = get_user_model()

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Mostrar el perfil del usuario autenticado.
        """
        return ProfileService.get_authenticated_user(request)

    def put(self, request):
        """
        Actualizar el perfil del usuario autenticado.
        """
        serializer = UpdateProfileSerializer(
            instance=request.user,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            # Retornar perfil actualizado con relaciones
            return ProfileService.get_authenticated_user(request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
