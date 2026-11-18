from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra):
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra)


class User(AbstractUser):
    """A donor. Signs in with email; `name` is the full name shown on receipts."""

    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.name} <{self.email}>"

    @property
    def public_name(self):
        """First name and last initial, e.g. "Sara A.", for public donation lists."""
        parts = self.name.split()
        if not parts:
            return "A donor"
        if len(parts) == 1:
            return parts[0]
        return f"{parts[0]} {parts[-1][0]}."
