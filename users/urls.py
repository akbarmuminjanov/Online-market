from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password-change/", PasswordChangeView.as_view(template_name="registration/password_change.html"), name="password_change"),
    path("password-change-done/", PasswordChangeDoneView.as_view(template_name="registration/password_ch_done.html"), name="password_change_done"),
]
