# HU02_ProfileManagement/forms/update_profile_form.py

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password

User = get_user_model()

class UpdateProfileForm(forms.Form):
    document_number = forms.CharField(max_length=20, required=False)
    name = forms.CharField(max_length=255, required=False)
    paternal_lastname = forms.CharField(max_length=255, required=False)
    maternal_lastname = forms.CharField(max_length=255, required=False)
    email = forms.EmailField(required=False)
    user_name = forms.CharField(max_length=150, required=False)
    current_password = forms.CharField(required=False)
    password = forms.CharField(min_length=8, required=False)
    sex = forms.CharField(max_length=1, required=False)
    phone = forms.CharField(max_length=100, required=False)
    document_type_id = forms.IntegerField(required=False)
    country_id = forms.IntegerField(required=False)

    def __init__(self, data, user):
        super().__init__(data)
        self.user = user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.exclude(pk=self.user.pk).filter(email=email, deleted_at__isnull=True).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        return email

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if user_name and User.objects.exclude(pk=self.user.pk).filter(user_name=user_name, deleted_at__isnull=True).exists():
            raise ValidationError("El nombre de usuario ya está en uso.")
        return user_name

    def clean_document_number(self):
        doc = self.cleaned_data.get('document_number')
        if doc and User.objects.exclude(pk=self.user.pk).filter(document_number=doc, deleted_at__isnull=True).exists():
            raise ValidationError("El número de documento ya está registrado.")
        return doc

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") and not cleaned_data.get("current_password"):
            raise ValidationError({"current_password": "La contraseña actual es obligatoria para cambiar la nueva."})

        if cleaned_data.get("password") and not check_password(cleaned_data["current_password"], self.user.password):
            raise ValidationError({"current_password": "La contraseña actual es incorrecta."})

        return cleaned_data
