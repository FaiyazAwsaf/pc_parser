from django.urls import path
from .views import (
    HelloView,
    UserRegistrationView,
    UserLoginView,
    EmailVerificationView,
    ResendVerificationView,
    UserProfileView,
    LogoutView,
)

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("verify-email/", EmailVerificationView.as_view(), name="verify-email"),
    path(
        "resend-verification/",
        ResendVerificationView.as_view(),
        name="resend-verification",
    ),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("logout/", LogoutView.as_view(), name="user-logout"),
]
