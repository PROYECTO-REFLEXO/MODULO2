from django.urls import path, include
from .views import (
    # User views
    UserDetailView, UserUpdateView, UserProfilePhotoView, UserSearchView, UserProfileView,
    
    # Profile views
    ProfileDetailView, ProfileUpdateView, ProfileCreateView, PublicProfileView,
    ProfileSettingsView, ProfileCompletionView, ProfileSearchView,
    
    # Password views
    PasswordChangeView, PasswordResetView, PasswordResetConfirmView,
    PasswordStrengthView, PasswordHistoryView, PasswordPolicyView,
    
    # Verification views
    VerificationCodeView, EmailChangeView, EmailChangeConfirmView,
    VerificationCodeResendView, VerificationStatusView,
    EmailVerificationView, EmailVerificationConfirmView
)

app_name = 'users_profiles'

urlpatterns = [
    # User management endpoints
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('user/update/', UserUpdateView.as_view(), name='user-update'),
    path('user/photo/', UserProfilePhotoView.as_view(), name='user-photo'),
    path('user/search/', UserSearchView.as_view(), name='user-search'),
    path('user/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    
    # Profile management endpoints
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/create/', ProfileCreateView.as_view(), name='profile-create'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/settings/', ProfileSettingsView.as_view(), name='profile-settings'),
    path('profile/completion/', ProfileCompletionView.as_view(), name='profile-completion'),
    path('profile/search/', ProfileSearchView.as_view(), name='profile-search'),
    path('profile/<str:username>/', PublicProfileView.as_view(), name='public-profile'),
    
    # Password management endpoints
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),
    path('password/reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password/strength/', PasswordStrengthView.as_view(), name='password-strength'),
    path('password/history/', PasswordHistoryView.as_view(), name='password-history'),
    path('password/policy/', PasswordPolicyView.as_view(), name='password-policy'),
    
    # Verification endpoints
    path('verification/code/', VerificationCodeView.as_view(), name='verification-code'),
    path('verification/email/change/', EmailChangeView.as_view(), name='email-change'),
    path('verification/email/change/confirm/', EmailChangeConfirmView.as_view(), name='email-change-confirm'),
    path('verification/code/resend/', VerificationCodeResendView.as_view(), name='verification-code-resend'),
    path('verification/status/', VerificationStatusView.as_view(), name='verification-status'),
    path('verification/email/', EmailVerificationView.as_view(), name='email-verification'),
    path('verification/email/confirm/', EmailVerificationConfirmView.as_view(), name='email-verification-confirm'),
]
