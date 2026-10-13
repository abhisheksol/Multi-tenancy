from blog.models import Post

from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.handlers.create_post_handler import CreatePostHandler
from blog.handlers.create_user_handler import CreateUserHandler



from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.handlers.create_user_handler import (
    CreateUserHandler,
)


class UserRegistrationSerializer(
    serializers.ModelSerializer
):
    onboarding_token = serializers.CharField(
        write_only=True
    )
    tenant_name = serializers.CharField(
        write_only=True,
        max_length=100,
    )
    tenant_subdomain = serializers.CharField(
        write_only=True,
        max_length=50,
    )

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "onboarding_token",
            "tenant_name",
            "tenant_subdomain",
        ]
        read_only_fields = [
            "id",
            "username",
            "email",
        ]

    def validate(self, attrs):
        return CreateUserHandler().validate(attrs)

    def create(self, validated_data):
        return CreateUserHandler().create(
            validated_data
        )






class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        handler = CreatePostHandler()
        request = self.context["request"]

        return handler.validate(attrs, request.user)

    def create(self, validated_data):
        handler = CreatePostHandler()
        request = self.context["request"]

        return handler.create(validated_data, request.user)




from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from blog.handlers.login_handler import LoginHandler


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    tenant_subdomain = serializers.CharField()

    def validate(self, attrs):
        handler = LoginHandler()
        return handler.validate(attrs)

    def create(self, validated_data):
        user = validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }






from blog.handlers.ldap_login_handler import (
    LDAPLoginHandler,
)


class LDAPLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):
        return LDAPLoginHandler().validate(attrs)

    def create(self, validated_data):
        return LDAPLoginHandler().create(
            validated_data
        )
