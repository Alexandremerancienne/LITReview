from django.contrib.auth.models import AbstractUser


class AppUser(AbstractUser):
    """A class to represent a User.
    AppUser inherits from AbstractUser class."""

    pass

    def __str__(self):
        return self.username
