from blog.models import Post

from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.handlers.create_post_handler import CreatePostHandler
from blog.handlers.create_user_handler import CreateUserHandler


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    tenant_subdomain = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "password",
            "tenant_subdomain",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        handler = CreateUserHandler()
        return handler.validate(attrs)

    def create(self, validated_data):
        handler = CreateUserHandler()
        return handler.create(validated_data)





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
