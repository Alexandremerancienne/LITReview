from django.contrib.auth.forms import UserCreationForm
from .models import AppUser


class CreateUserForm(UserCreationForm):
    class Meta:
        model = AppUser
        fields = ["username", "email", "password1", "password2"]
