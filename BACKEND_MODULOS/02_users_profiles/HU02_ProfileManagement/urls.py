from django.urls import path
from HU02_ProfileManagement.controllers.profile_controller import ProfileView
from HU02_ProfileManagement.controllers.image_controller import (
    UploadUserPhotoView,
    ShowUserPhotoView,
    DeleteUserPhotoView
)

urlpatterns = [
    # Perfil del usuario autenticado
    path('me/', ProfileView.as_view(), name='user_profile'),

    # Foto de perfil
    path('photo/<int:user_id>/upload/', UploadUserPhotoView.as_view(), name='upload_user_photo'),
    path('photo/<int:user_id>/', ShowUserPhotoView.as_view(), name='show_user_photo'),
    path('photo/<int:user_id>/delete/', DeleteUserPhotoView.as_view(), name='delete_user_photo'),
]
