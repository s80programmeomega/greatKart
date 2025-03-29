
from django.http import HttpRequest

from .models import Category


def get_categories(request: HttpRequest):
    categories = Category.objects.all()
    return {'categories':categories}