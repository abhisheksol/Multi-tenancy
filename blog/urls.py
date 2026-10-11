
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from blog.views import (
    LoginView,
    UserRegistrationView,
    PostListCreateView,
    PostDetailView,
)

urlpatterns = [
    path(
        "auth/register/",
        UserRegistrationView.as_view(),
        name="register",
    ),
    path("auth/login/", LoginView.as_view(), name="login"),
    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "posts/",
        PostListCreateView.as_view(),
        name="post-list-create",
    ),
    path(
        "posts/<int:pk>/",
        PostDetailView.as_view(),
        name="post-detail",
    ),
]
