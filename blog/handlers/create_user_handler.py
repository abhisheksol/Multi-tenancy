
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

from blog.models import Tenant


class CreateUserHandler:

    def validate(self, data):
        subdomain = data.get("tenant_subdomain", "").strip().lower()

        if not subdomain:
            raise ValidationError({
                "tenant_subdomain": "Subdomain is required."
            })

        # Only allow a single DNS-label-style subdomain.
        if (
            len(subdomain) > 50
            or slugify(subdomain) != subdomain
            or "." in subdomain
        ):
            raise ValidationError({
                "tenant_subdomain": "Enter a valid subdomain."
            })

        if Tenant.objects.filter(subdomain=subdomain).exists():
            raise ValidationError({
                "tenant_subdomain": "This subdomain is already taken."
            })

        data["tenant_subdomain"] = subdomain
        return data

    @transaction.atomic
    def create(self, validated_data):
        User = get_user_model()

        subdomain = validated_data.pop("tenant_subdomain")
        password = validated_data.pop("password")

        tenant = Tenant.objects.create(
            name=f"{subdomain.title()} Organization",
            subdomain=subdomain,
            is_active=True,
        )

        user = User.objects.create_user(
            password=password,
            tenant=tenant,
            **validated_data,
        )

        return user
