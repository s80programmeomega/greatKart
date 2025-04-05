from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import UserProfile, CustomUser


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }


class UserSignUpForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'title', 'first_name', 'last_name',
                  'phone_number', 'address', 'city', 'state', 'country', 'zip_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Replace the 'user' field with a hyperlink
        if self.instance and self.instance.user:
            user_update_url = reverse('accounts:update_user', kwargs={
                                      'pk': self.instance.user.pk})
            self.fields['user'] = forms.CharField(
                label='User',
                required=False,
                widget=forms.TextInput(attrs={
                    'readonly': 'readonly',
                    'value': f'{self.instance.user.username}',
                })
            )
            # Add the hyperlink to the field's help text
            self.fields['user'].help_text = mark_safe(
                f'<a href="{user_update_url}">Click here to update user details</a>')

    def save(self, user, *args, **kwargs):
        profile = super().save(commit=False)
        profile.user = user  # Set the user to the currently logged-in user
        if kwargs.get('commit', True):
            profile.save()
        return profile


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
