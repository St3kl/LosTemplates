from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)

from django import forms

from django.contrib.auth.models import User

from .models import UserProfile


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
    )

    class Meta:

        model = User

        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):

        email = self.cleaned_data["email"].lower()

        if User.objects.filter(
            email=email,
        ).exists():

            raise forms.ValidationError(
                "This email is already registered.",
            )

        return email


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        max_length=150,
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
    )
    
class UserUpdateForm(forms.ModelForm):

    class Meta:

        model = User

        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )


class ProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        fields = (
            "avatar",
            "bio",
            "country",
        )    