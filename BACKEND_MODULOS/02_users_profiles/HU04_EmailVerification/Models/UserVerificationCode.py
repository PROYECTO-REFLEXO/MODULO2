# your_app/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone

class UserVerificationCode(models.Model):
    class Meta:
        db_table = 'user_verification_code'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='verification_codes'
    )
    code = models.CharField(max_length=10)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self) -> bool:
        return timezone.now() > self.expires_at
