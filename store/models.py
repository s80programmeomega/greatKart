from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from category.models import Category


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True, blank=False)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.FloatField()
    product_image = models.ImageField(
        upload_to="photos/products/", default="defaults/default_product.jpg", blank=True)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse("product_detail", args=[self.category.slug, self.slug])

    def get_absolute_url(self):
        return self.get_url()

    class Meta:
        ordering = ('-date_added',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(
            variation_category="color", is_active=True
        )

    def sizes(self):
        return super(VariationManager, self).filter(
            variation_category="size", is_active=True
        )


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100,
        choices=(
            ("color", "color"),
            ("size", "size"),
        ),
    )
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
