
from django.core import signing

from blog.services.ldap_service import LDAPService


ONBOARDING_SALT = "blog.ldap.onboarding.v1"


class LDAPLoginHandler:

    def validate(self, data):
        profile = LDAPService().authenticate(
            username=data["username"],
            password=data["password"],
        )

        data["ldap_profile"] = profile
        return data

    def create(self, validated_data):
        profile = validated_data["ldap_profile"]

        token = signing.dumps(
            {
                "purpose": "tenant_registration",
                "username": profile["username"],
            },
            salt=ONBOARDING_SALT,
        )

        return {
            "onboarding_token": token,
            "expires_in": 600,
            "user": profile,
        }
