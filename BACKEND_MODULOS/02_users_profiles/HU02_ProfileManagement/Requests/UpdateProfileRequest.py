from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UpdateProfileSerializer(serializers.Serializer):
    document_number = serializers.CharField(
        max_length=20, required=False)
    photo_url = serializers.URLField(required=False, allow_null=True)
    name = serializers.CharField(max_length=255, required=False)
    paternal_lastname = serializers.CharField(max_length=255, required=False)
    maternal_lastname = serializers.CharField(
        max_length=255, required=False, allow_null=True)
    email = serializers.EmailField(max_length=255, required=False)
    sex = serializers.CharField(min_length=1, max_length=1, required=False)
    phone = serializers.CharField(max_length=100, required=False, allow_null=True)
    user_name = serializers.CharField(max_length=150, required=False, allow_null=True)
    current_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(min_length=8, write_only=True, required=False)
    document_type_id = serializers.IntegerField(required=False)
    country_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_document_number(self, value):
        user = self.context['request'].user
        if User.objects.filter(document_number=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError('El número de documento ya está registrado.')
        return value

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError('El correo electrónico ya está registrado.')
        return value

    def validate_user_name(self, value):
        user = self.context['request'].user
        if User.objects.filter(user_name=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError('El nombre de usuario ya está en uso.')
        return value

    def validate(self, attrs):
        pwd = attrs.get('password')
        current = attrs.get('current_password')
        if pwd:
            if not current:
                raise serializers.ValidationError({'current_password': 'current_password is required when changing password.'})
            user = self.context['request'].user
            if not user.check_password(current):
                raise serializers.ValidationError({'current_password': 'La contraseña actual es incorrecta.'})
            # hash new password
            attrs['password'] = make_password(pwd)
        return attrs

    def update(self, instance, validated_data):
        # instance is the User
        for attr, value in validated_data.items():
            if attr in ['current_password']:
                continue
            setattr(instance, attr, value)
        instance.save()
        return instance
