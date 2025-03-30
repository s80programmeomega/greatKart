from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Product


@receiver(post_save, sender=Product)
def set_default_product_image(sender, instance: Product, **kwargs):
    # Check if the product has no image
    if not instance.product_image:
        Product.objects.filter(pk=instance.pk).update(
            product_image="defaults/default_product.jpg"
        )
