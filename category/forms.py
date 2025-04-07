from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'category_name': 'Category Name',
            'slug': 'Slug',
            'description': 'Description',
        }
        help_texts = {
            'category_name': 'Enter the name of the category.',
            'slug': 'Leave blank to auto-generate.',
            'description': 'Provide a brief description of the category.',
        }
