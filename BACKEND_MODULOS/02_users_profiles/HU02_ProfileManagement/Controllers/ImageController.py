from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import FileResponse, Http404
from django.conf import settings
from django.utils.crypto import get_random_string
import os

from your_app.serializers.update_photo_serializer import UpdatePhotoSerializer

User = get_user_model()

class UploadUserPhotoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, user_id):
        serializer = UpdatePhotoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(pk=user_id)

                # Eliminar foto antigua si existe
                old_path = user.photo_url
                if old_path:
                    full_old = os.path.join(settings.MEDIA_ROOT, old_path)
                    if os.path.exists(full_old):
                        os.remove(full_old)

                # Guardar nueva foto
                file = serializer.validated_data.get('photo')
                file_ext = file.name.split('.')[-1]
                random_name = get_random_string(length=15)
                file_name = f"{random_name}.{file_ext}"
                file_path = default_storage.save(f"images/users/{file_name}", ContentFile(file.read()))

                user.photo_url = file_path
                user.save()

                return Response({
                    'message': 'Foto actualizada correctamente',
                    'photo_url': file_path,
                    'full_url': request.build_absolute_uri(settings.MEDIA_URL + file_path),
                    'file_name': file_name
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShowUserPhotoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            path = user.photo_url
n            if not path:
                raise Http404('Imagen no encontrada')

            full_path = os.path.join(settings.MEDIA_ROOT, path)
            if not os.path.exists(full_path):
                raise Http404('Imagen no encontrada')

            # Content type dinámico según extensión
            ext = path.split('.')[-1].lower()
            content_type = f'image/{ext if ext != "jpg" else "jpeg"}'
            return FileResponse(open(full_path, 'rb'), content_type=content_type)
        except User.DoesNotExist:
            raise Http404('Usuario no encontrado')

class DeleteUserPhotoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            path = user.photo_url
            if path:
                full_path = os.path.join(settings.MEDIA_ROOT, path)
                if os.path.exists(full_path):
                    os.remove(full_path)
                user.photo_url = None
                user.save()
                return Response({'message': 'Foto eliminada correctamente'}, status=status.HTTP_200_OK)
            return Response({'message': 'No hay foto para eliminar'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
