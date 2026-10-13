import re

import ldap
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class LDAPService:

    def authenticate(self, username, password):
        error = "Invalid LDAP credentials."

        if not re.fullmatch(
            r"[a-zA-Z0-9][a-zA-Z0-9._-]{0,149}",
            username or "",
        ):
            raise AuthenticationFailed(error)

        if not password:
            raise AuthenticationFailed(error)

        user_dn = (
            f"uid={username},"
            "ou=users,dc=example,dc=org"
        )

        connection = ldap.initialize(
            settings.AUTH_LDAP_SERVER_URI
        )
        connection.set_option(ldap.OPT_NETWORK_TIMEOUT, 5)

        try:
            connection.simple_bind_s(user_dn, password)

            results = connection.search_s(
                user_dn,
                ldap.SCOPE_BASE,
                "(objectClass=*)",
                ["uid", "cn", "mail"],
            )

            if not results:
                raise AuthenticationFailed(error)

            attributes = results[0][1]

            def get_attribute(name):
                values = attributes.get(name, [])
                return (
                    values[0].decode("utf-8")
                    if values else ""
                )

            return {
                "username": get_attribute("uid"),
                "email": get_attribute("mail"),
                "name": get_attribute("cn"),
            }

        except ldap.INVALID_CREDENTIALS:
            raise AuthenticationFailed(error)

        except ldap.LDAPError:
            raise AuthenticationFailed(
                "LDAP service is unavailable."
            )

        finally:
            connection.unbind_s()