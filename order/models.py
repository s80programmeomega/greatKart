import uuid

from django.contrib.auth import get_user_model
from django.db import models


class Payment(models.Model):
    payment_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name="payment",
                             )
    payment_method = models.CharField(
        max_length=100,
        choices=(
            ("PayPal", "PayPal"),
            ("Stripe", "Stripe"),
            ("Razorpay", "Razorpay"),
        ),
    )
    amount_paid = models.FloatField()
    status = models.CharField(
        max_length=100,
        choices=(
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Failed", "Failed"),
        ),
    )
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.payment_method


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        NEW = 'New', 'New'
        ACCEPTED = 'Accepted', 'Accepted'
        COMPLETED = 'Completed', 'Completed'
        CANCELLED = 'Cancelled', 'Cancelled'

    class Countries(models.TextChoices):
        USA = 'USA', 'United States'
        CANADA = 'Canada', 'Canada'
        UK = 'UK', 'United Kingdom'
        AUSTRALIA = 'Australia', 'Australia'
        INDIA = 'India', 'India'
        FRANCE = 'France', 'France'
        GERMANY = 'Germany', 'Germany'
        ITALY = 'Italy', 'Italy'
        SPAIN = 'Spain', 'Spain'
        BRAZIL = 'Brazil', 'Brazil'
        OTHER = 'Other', 'Other'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    order_number = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, choices=Countries.choices, default=Countries.USA)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(
        max_length=100, choices=StatusChoices.choices, default=StatusChoices.NEW)
    ip = models.CharField(max_length=20, blank=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.profile.first_name if self.user.profile.first_name else self.user.username


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE)
    variation = models.ForeignKey(
        "store.Variation",
        on_delete=models.CASCADE,
    )
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    is_ordered = models.BooleanField(default=False)

    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
