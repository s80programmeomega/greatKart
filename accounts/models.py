import os
from io import BytesIO
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (AbstractBaseUser, AnonymousUser,
                                        BaseUserManager, PermissionsMixin)
from django.core.files.base import ContentFile
from django.db import models, transaction
from PIL import Image


class UserType(models.TextChoices):
    GUEST = "GUEST", "Guest"
    CUSTOMER = "CUSTOMER", "Customer"
    ADMIN = "ADMIN", "Admin"


class CustomUserManager(BaseUserManager):
    """Define a model manager for CustomUser model."""

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("user_type", UserType.CUSTOMER)
        if not extra_fields.get("user_type"):
            extra_fields["user_type"] = UserType.CUSTOMER
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)

        # Use transaction.atomic to ensure both User and UserProfile are created together
        with transaction.atomic():
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)

            # create the associated user profile
            userprofile = UserProfile.objects.create(user=user)

        return user, userprofile

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

    username = models.CharField(max_length=50, unique=True, blank=True)
    email = models.EmailField(
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def get_profile_url(self):
        """
        Returns the URL for the user's profile page.
        """
        return reverse('accounts:profile', kwargs={'pk': self.pk})

    def __str__(self):
        return self.username


class CustomAnonymousUser(AnonymousUser):
    def __init__(self):
        super().__init__()
        self.user_type = UserType.GUEST

    @property
    def user_type(self):
        return self.user_type

    @user_type.setter
    def user_type(self, value):
        self.user_type = value


class UserProfile(models.Model):
    profile_picture = models.ImageField(
        upload_to="accounts/profile_pictures/", blank=True, null=True
    )
    thumbnail = models.ImageField(
        upload_to="accounts/profile_thumbnails/", blank=True, null=True
    )

    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="profile"
    )

    bio = models.TextField(blank=True, verbose_name="About Me")
    title = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)

    def generate_thumbnail(self):
        if self.profile_picture:
            # Open the uploaded image
            img = Image.open(self.profile_picture)

            # Check if the image is larger than the desired thumbnail size
            thumbnail_size = (150, 150)  # Set the desired thumbnail size
            if img.height > thumbnail_size[0] or img.width > thumbnail_size[1]:
                # Create a thumbnail
                img.thumbnail(thumbnail_size)

                # Save the thumbnail to a BytesIO object
                thumb_io = BytesIO()
                img.save(thumb_io, format=img.format)

                filename = os.path.basename(self.profile_picture.name)

                # Save the thumbnail to the thumbnail field
                self.thumbnail.save(
                    f"thumbnail_{filename}",
                    ContentFile(thumb_io.getvalue()),
                    save=False,
                )

            # Close the image file
            img.close()

    def clear_thumbnail(self):
        # If the profile picture is removed, clear the thumbnail
        if not self.profile_picture and self.thumbnail:
            print(f"===> Clearing thumbnail {self.thumbnail} <===")
            self.thumbnail.delete(save=False)
            self.thumbnail = None

    def __str__(self):
        return self.user.username
