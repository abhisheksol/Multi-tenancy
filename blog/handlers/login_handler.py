
from django_auth_ldap.backend import LDAPBackend

from rest_framework.exceptions import AuthenticationFailed

from blog.models import Tenant


class LoginHandler:

    def validate(self, data):
        username = data["username"].strip()
        password = data["password"]
        subdomain = data[
            "tenant_subdomain"
        ].strip().lower()

        error = "Invalid credentials or tenant."

        try:
            tenant = Tenant.objects.get(
                subdomain=subdomain,
                is_active=True,
            )
        except Tenant.DoesNotExist:
            raise AuthenticationFailed(error)

        # Authenticate against LDAP.
        user = LDAPBackend().authenticate(
            request=None,
            username=username,
            password=password,
        )

        if user is None or not user.is_active:
            raise AuthenticationFailed(error)

        # Verify Django tenant ownership.
        if user.tenant_id != tenant.id:
            raise AuthenticationFailed(error)

        data["user"] = user
        return data
