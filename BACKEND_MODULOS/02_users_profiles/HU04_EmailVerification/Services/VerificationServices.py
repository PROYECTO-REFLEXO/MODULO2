# your_app/services/verification_service.py

import logging
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from your_app.models import UserVerificationCode

User = get_user_model()
logger = logging.getLogger(__name__)

class VerificationService:
    @staticmethod
    def verify_code(user: User, code: str) -> tuple[dict, int]:
        """
        Orquesta la verificación de un código de usuario:
        1) Obtiene el último código válido bajo bloqueo SELECT FOR UPDATE.
        2) Lo valida.
        3) Si es válido, maneja la verificación exitosa.
           Si no, retorna la respuesta de error.
        """
        # Bloquea la fila para evitar race conditions
        latest_code = (
            UserVerificationCode.objects
            .select_for_update()
            .filter(user=user)
            .order_by('-expires_at')
            .first()
        )

        verif = VerificationService._validation_verify(latest_code, user, code)
        if verif['valid']:
            return VerificationService._handle_successful_verification(user, latest_code)
        return verif, 400

    @staticmethod
    def _validation_verify(
        code_obj: UserVerificationCode | None,
        user: User,
        code: str
    ) -> dict:
        """
        Comprueba que:
        - Exista un código para el usuario.
        - Coincida con el enviado.
        - No esté bloqueado.
        - No haya expirado.
        En caso de fallo, incrementa intentos fallidos y devuelve error.
        """
        if not code_obj:
            VerificationService._increment_failed_attempts(user)
            return VerificationService._invalid_response(
                'code_not_found',
                'No se encontró un código válido para este usuario.'
            )

        if code_obj.code != code:
            VerificationService._increment_failed_attempts(user)
            return VerificationService._invalid_response(
                'code_mismatch',
                'El código ingresado no coincide.'
            )

        if code_obj.locked_until and timezone.now() < code_obj.locked_until:
            return VerificationService._invalid_response(
                'code_locked',
                'Demasiados intentos fallidos. Intenta nuevamente en 10 minutos.'
            )

        if code_obj.is_expired():
            code_obj.delete()
            VerificationService._increment_failed_attempts(user)
            return VerificationService._invalid_response(
                'code_expired',
                'El código ha expirado.'
            )

        return {'valid': True, 'message': 'Código validado.'}

    @staticmethod
    def _handle_successful_verification(
        user: User,
        code_obj: UserVerificationCode
    ) -> tuple[dict, int]:
        """
        Dentro de una transacción:
        - Borra todos los códigos (por seguridad).
        - Si ya existe un token DRF, lo retorna.
        - Si no, crea uno nuevo.
        - Retorna también el rol del usuario.
        """
        try:
            with transaction.atomic():
                # Eliminar todos los códigos (por seguridad)
                UserVerificationCode.objects.filter(user=user).delete()

                # Actualizar estado del usuario (p.ej. marcar verificado)
                user.is_verified = True
                user.save()

                # Reusar o crear token
                token_obj, created = Token.objects.get_or_create(user=user)
                token = token_obj.key

                # Obtener primer rol si lo hay (ajusta según tu modelo)
                roles = getattr(user, 'roles', None)
                role_id = None
                if roles is not None:
                    first_role = roles.first()
                    role_id = first_role.id if first_role else None

            return (
                {
                    'valid': True,
                    'message': 'Código válido.',
                    'token': token,
                    'role': role_id,
                },
                200
            )
        except Exception as e:
            logger.error('Error al verificar código', exc_info=e, extra={
                'user_id': user.id,
                'code': getattr(code_obj, 'code', None),
            })
            resp = VerificationService._invalid_response(
                'internal_error',
                'Error interno al procesar el código.',
                error_message=str(e)
            )
            return resp, 500

    @staticmethod
    def _increment_failed_attempts(user: User) -> None:
        """
        Incrementa el contador en el último UserVerificationCode
        y bloquea si supera 3 intentos.
        """
        code_obj = (
            UserVerificationCode.objects
            .filter(user=user)
            .order_by('-created_at')
            .first()
        )
        if not code_obj:
            return

        code_obj.failed_attempts = (code_obj.failed_attempts or 0) + 1
        if code_obj.failed_attempts >= 3:
            code_obj.locked_until = timezone.now() + timezone.timedelta(minutes=10)
        code_obj.save()

    @staticmethod
    def _invalid_response(
        reason: str,
        message: str,
        error_message: str | None = None
    ) -> dict:
        """
        Retorna un dict estándar para errores:
        {
          'valid': False,
          'reason': <código>,
          'message': <mensaje>,
          ['error_message': <detalle opcional>]
        }
        """
        resp = {
            'valid': False,
            'reason': reason,
            'message': message,
        }
        if error_message:
            resp['error_message'] = error_message
        return resp
