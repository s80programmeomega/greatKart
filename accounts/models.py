from django.contrib.auth.models import (
    AbstractBaseUser,
    AnonymousUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserType(models.TextChoices):
    GUEST = "GUEST", "Guest"
    CUSTOMER = "CUSTOMER", "Customer"
    ADMIN = "ADMIN", "Admin"


class CustomUserManager(BaseUserManager):
    """Define a model manager for CustomUser model with no username field."""

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("user_type", UserType.CUSTOMER)
        if not extra_fields.get("user_type"):
            extra_fields["user_type"] = UserType.CUSTOMER
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("user_type", UserType.ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("user_type"):
            extra_fields["user_type"] = UserType.ADMIN
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email as the unique identifier."""

    user_type = models.CharField(
        max_length=20, choices=UserType.choices, default=UserType.CUSTOMER, blank=True
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name",]


    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email


class CustomAnonymousUser(AnonymousUser):
    def __init__(self):
        super().__init__()
        self._user_type = UserType.GUEST

    @property
    def user_type(self):
        return self._user_type

    @user_type.setter
    def user_type(self, value):
        self._user_type = value
