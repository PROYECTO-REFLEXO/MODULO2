from rest_framework import serializers
from django.core.files.images import get_image_dimensions

class UpdatePhotoSerializer(serializers.Serializer):
    photo = serializers.ImageField(
        required=False,
        allow_null=True,
    )

    def validate_photo(self, image):
        # Permitir valor nulo
        if image is None:
            return None

        # Validar tipo MIME
        valid_mimes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        content_type = image.content_type
        if content_type not in valid_mimes:
            raise serializers.ValidationError(
                'La imagen debe ser de tipo: jpeg, png, jpg, gif o webp.'
            )

        # Validar tamaño máximo (5MB)
        max_size = 5 * 1024 * 1024  # 5MB en bytes
        if image.size > max_size:
            raise serializers.ValidationError(
                'La imagen no debe superar los 5MB.'
            )

        # Validar dimensiones
        width, height = get_image_dimensions(image)
        if width < 100 or height < 100 or width > 2000 or height > 2000:
            raise serializers.ValidationError(
                'La imagen debe tener un mínimo de 100x100px y máximo de 2000x2000px.'
            )

        return image
