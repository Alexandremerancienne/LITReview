from django.urls import path
from accounts import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
]
