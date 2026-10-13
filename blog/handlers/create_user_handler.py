
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import signing
from django.db import transaction
from django.utils.text import slugify

from rest_framework.exceptions import ValidationError

from blog.models import Tenant
from blog.handlers.ldap_login_handler import (
    ONBOARDING_SALT,
)
from blog.services.ldap_service import LDAPService


class CreateUserHandler:

    def validate(self, data):
        token = data.get("onboarding_token", "")

        try:
            payload = signing.loads(
                token,
                salt=ONBOARDING_SALT,
                max_age=settings.LDAP_ONBOARDING_TOKEN_MAX_AGE,
            )
        except (
            signing.BadSignature,
            signing.SignatureExpired,
            TypeError,
            ValueError,
        ):
            raise ValidationError({
                "onboarding_token":
                    "Invalid or expired onboarding token."
            })

        if payload.get("purpose") != "tenant_registration":
            raise ValidationError({
                "onboarding_token": "Invalid token purpose."
            })

        username = payload.get("username")

        if not isinstance(username, str) or not username:
            raise ValidationError({
                "onboarding_token": "Invalid user identity."
            })

        subdomain = data["tenant_subdomain"].strip().lower()
        tenant_name = data["tenant_name"].strip()

        if (
            not subdomain
            or len(subdomain) > 50
            or slugify(subdomain) != subdomain
            or subdomain.startswith("-")
            or subdomain.endswith("-")
        ):
            raise ValidationError({
                "tenant_subdomain": "Invalid subdomain."
            })

        if not tenant_name:
            raise ValidationError({
                "tenant_name": "Tenant name is required."
            })

        if Tenant.objects.filter(
            subdomain=subdomain
        ).exists():
            raise ValidationError({
                "tenant_subdomain":
                    "This subdomain is already taken."
            })

        User = get_user_model()

        if User.objects.filter(
            username=username
        ).exists():
            raise ValidationError({
                "onboarding_token":
                    "This LDAP user is already registered."
            })

        data["ldap_username"] = username
        data["tenant_subdomain"] = subdomain
        data["tenant_name"] = tenant_name

        return data

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data["ldap_username"]

        # We already verified the LDAP password
        # when issuing the onboarding token.
        # No LDAP password is stored here.

        tenant = Tenant.objects.create(
            name=validated_data["tenant_name"],
            subdomain=validated_data["tenant_subdomain"],
            is_active=True,
        )

        User = get_user_model()

        user = User.objects.create_user(
            username=username,
            email="",
            password=None,
            tenant=tenant,
        )

        return user
