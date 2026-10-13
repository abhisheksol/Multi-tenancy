
from rest_framework import generics
from rest_framework.permissions import AllowAny

from blog.models import Post
from blog.serializers import UserRegistrationSerializer
from blog.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated






class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(
            tenant=self.request.user.tenant
        )


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(
            tenant=self.request.user.tenant
        )




from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from blog.serializers import LoginSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.save()

        return Response(tokens)




from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from blog.serializers import LDAPLoginSerializer


class LDAPLoginView(generics.GenericAPIView):
    serializer_class = LDAPLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        result = serializer.save()
        return Response(result)
