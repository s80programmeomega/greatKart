from django import forms


from .models import Order, OrderProduct, Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            "user",
            # "payment_id",
            "payment_method",
            "amount_paid",
            "status",
        ]
        widgets = {
            "user": forms.Select(attrs={"class": "form-control"}),
            # "payment_id": forms.TextInput(attrs={"class": "form-control"}),
            "payment_method": forms.Select(attrs={"class": "form-control"}),
            "amount_paid": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "address_line_1",
            "address_line_2",
            "country",
            "state",
            "city",
            "order_note",
            # "ip"
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "address_line_1": forms.TextInput(attrs={"class": "form-control"}),
            "address_line_2": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.Select(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "order_note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Order Note (optional)",
                }
            ),
        }


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = [
            "order",
            "payment",
            "user",
            "product",
            "quantity",
            "price",
            "is_ordered",
        ]
        widgets = {
            "order": forms.Select(attrs={"class": "form-control"}),
            "payment": forms.Select(attrs={"class": "form-control"}),
            "user": forms.Select(attrs={"class": "form-control"}),
            "product": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "is_ordered": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
