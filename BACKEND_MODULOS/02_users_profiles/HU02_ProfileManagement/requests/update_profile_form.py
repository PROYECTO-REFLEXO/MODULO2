# HU02_ProfileManagement/forms/update_profile_form.py

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UpdateProfileForm(forms.Form):
    """
    Equivalente a UpdateProfileRequest de Laravel.
    Permite validar actualización de datos del perfil del usuario autenticado.
    """

    document_number = forms.CharField(
        max_length=20, required=False
    )
    photo_url = forms.URLField(required=False)
    name = forms.CharField(max_length=255, required=False)
    paternal_lastname = forms.CharField(max_length=255, required=False)
    maternal_lastname = forms.CharField(max_length=255, required=False)
    email = forms.EmailField(max_length=255, required=False)
    sex = forms.CharField(max_length=1, required=False)
    phone = forms.CharField(max_length=100, required=False)
    user_name = forms.CharField(max_length=150, required=False)
    current_password = forms.CharField(required=False)
    password = forms.CharField(min_length=8, required=False)
    document_type_id = forms.IntegerField(required=False)
    country_id = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # usuario autenticado
        super().__init__(*args, **kwargs)

    def clean_document_number(self):
        doc = self.cleaned_data.get('document_number')
        if doc:
            exists = User.objects.filter(
                document_number=doc,
                deleted_at__isnull=True
            ).exclude(id=self.user.id).exists()
            if exists:
                raise forms.ValidationError('El número de documento ya está registrado.')
        return doc

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            exists = User.objects.filter(
                email=email,
                deleted_at__isnull=True
            ).exclude(id=self.user.id).exists()
            if exists:
                raise forms.ValidationError('El correo electrónico ya está registrado.')
        return email

    def clean_user_name(self):
        username = self.cleaned_data.get('user_name')
        if username:
            exists = User.objects.filter(
                user_name=username,
                deleted_at__isnull=True
            ).exclude(id=self.user.id).exists()
            if exists:
                raise forms.ValidationError('El nombre de usuario ya está en uso.')
        return username

    def clean(self):
        """
        Validaciones cruzadas, como required_with.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        current_password = cleaned_data.get('current_password')

        if password and not current_password:
            self.add_error('current_password', 'La contraseña actual es obligatoria para cambiar la nueva.')
