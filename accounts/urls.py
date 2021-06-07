from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password1.html"
        ),
        name="reset_password",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password2.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_forms.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password6.html"
        ),
        name="password_reset_complete",
    ),
]
