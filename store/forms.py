from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "product_image",
            "product_name",
            "slug",
            "description",
            "price",
            "stock",
            "is_available",
            "category",
        ]
        widgets = {
            "product_name": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "product_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
            "is_available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "product_name": "Product Name",
            "slug": "Slug",
            "description": "Product Description",
            "price": "Price",
            "product_image": "Product Image",
            "stock": "Stock",
            "is_available": "Is Available",
            "category": "Product Category",
        }
        help_texts = {
            "product_name": "Enter the name of the product.",
            "slug": "Enter a unique slug for the product or leave blank to auto-generate.",
            "description": "Enter a description of the product.",
            "price": "Enter the price of the product.",
            "product_image": "Upload an image of the product.",
            "stock": "Enter the stock quantity of the product.",
            "is_available": "Check if the product is available.",
            "category": "Select a category for the product.",
        }
