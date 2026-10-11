
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from blog.models import Tenant


class LoginHandler:

    def validate(self, data):
        subdomain = data.get("tenant_subdomain", "").strip().lower()

        try:
            tenant = Tenant.objects.get(
                subdomain=subdomain,
                is_active=True,
            )
        except Tenant.DoesNotExist:
            raise AuthenticationFailed(
                "Invalid credentials or tenant."
            )

        user = authenticate(
            username=data.get("username"),
            password=data.get("password"),
        )

        if user is None or not user.is_active:
            raise AuthenticationFailed(
                "Invalid credentials or tenant."
            )

        if user.tenant_id != tenant.id:
            raise AuthenticationFailed(
                "Invalid credentials or tenant."
            )

        data["user"] = user
        return data
