from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/enter_email.html'
         ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/email_sent.html'
         ),
         name='password_reset_done'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path("reset/done/", views.reset_done, name="reset_done"),
]
