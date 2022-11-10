from django.urls import path
from apps.authentication.views import LoginView, LogoutView, SignUpView, \
                                    PasswordResetView, PasswordResetDoneView , \
                                    PasswordResetConfirmView, PasswordResetCompleteView, \
                                    UserListView, UserDetailView

urlpatterns = [
    # Login/Signup/Logout urls
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # Urls users admin
    path("users/", UserListView.as_view(), name="users"),
    path("users/<int:pk>", UserDetailView.as_view(), name="users-detail"),

    # Password Reset
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", PasswordResetCompleteView.as_view(), name="password_reset_complete")
]
