from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.db.models import F, Value
from django.db.models.functions import Coalesce
from .models import UserProfile


def get_current_user_name(request: HttpRequest):
    if request.user.is_authenticated:
        # Use first_name if available, otherwise fallback to username
        display_name = request.user.profile.first_name or request.user.profile.last_name or request.user.username or request.user.email
    else:
        display_name = "Guest"  # Default value for unauthenticated users
    return {'display_name': display_name}
