
from rest_framework.exceptions import ValidationError

from blog.models import Post


class CreatePostHandler:

    def validate(self, data, user):
        if not user.tenant_id:
            raise ValidationError(
                "Your account is not assigned to a tenant."
            )

        if not user.tenant.is_active:
            raise ValidationError(
                "Your tenant is inactive."
            )

        return data

    def create(self, validated_data, user):
        return Post.objects.create(
            tenant=user.tenant,
            author=user,
            **validated_data,
        )
