
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from blog.views import (
    LDAPLoginView,
    UserRegistrationView,
    LoginView,
    PostListCreateView,
    PostDetailView,
)


urlpatterns = [
    path(
        "auth/ldap-login/",
        LDAPLoginView.as_view(),
        name="ldap-login",
    ),
    path(
        "auth/register/",
        UserRegistrationView.as_view(),
        name="register",
    ),
    path(
        "auth/login/",
        LoginView.as_view(),
        name="login",
    ),
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
