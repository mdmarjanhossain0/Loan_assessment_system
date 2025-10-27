from django.urls import path
from account.api.views import (
    RegisterView,
    LoginView,
    AccountDetailView,
    AccountUpdateView,
    ChangePasswordView,
    LogoutView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "account_api"



urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("properties", AccountDetailView.as_view(), name="account-details"),
    path("update", AccountUpdateView.as_view(), name="account-update"),
    path("change-password", ChangePasswordView.as_view(), name="change-password"),
    path("logout", LogoutView.as_view(), name="logout"),
]
