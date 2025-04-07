from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True, blank=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True)
    category_image = models.ImageField(
        upload_to="photos/categories", blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def get_url(self):
        return reverse("products_by_categories", args=[self.slug])

    def save(self, *args, **kwargs):
        # Automatically generate a slug from the name field
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.category_name
