from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from your_app.serializers.verification_serializer import VerificationSerializer
from your_app.services.verification_service import VerificationService

User = get_user_model()

class VerificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Valida el código de verificación del usuario autenticado.
        """
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user:
                return Response({'message': 'No se pudo determinar el usuario.'}, status=400)

            code = serializer.validated_data['code']
            result, status_code = VerificationService.verify_code(user, code)
            return Response(result, status=status_code)
        return Response(serializer.errors, status=400)

    def get(self, request):
        """
        Método index - no implementado.
        """
        return Response({'message': 'Método no implementado.'}, status=501)

    def put(self, request):
        """
        Método store (equivalente a PUT/actualizar) - no implementado.
        """
        return Response({'message': 'Método no implementado.'}, status=501)

    def patch(self, request):
        """
        Método create (parcial) - no implementado.
        """
        return Response({'message': 'Método no implementado.'}, status=501)
