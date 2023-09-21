from django.core.cache import cache
from django.core.mail import send_mail

import uuid
from typing import Any

from core import celery_app
from core.settings import CACHE_ONE_DAY, PROJECT_HTTP_ADDRESS


@celery_app.task
def send_confirmation_email(user: dict[str, Any]) -> None:
    token = uuid.uuid4()
    send_mail(
        subject="Email Confirmation",
        message=f"{PROJECT_HTTP_ADDRESS}/api/user/auth/confirm-email/{token}",
        from_email=None,
        recipient_list=[user["email"]],
    )
    cache.set(token, user, CACHE_ONE_DAY)


@celery_app.task
def send_reset_password_email(user: dict[str, Any]) -> None:
    token = uuid.uuid4()
    send_mail(
        subject="Reset Password",
        message=f"{PROJECT_HTTP_ADDRESS}/api/user/auth/reset-password/{token}",
        from_email=None,
        recipient_list=[user["email"]],
    )
    cache.set(token, user, CACHE_ONE_DAY)
