from django import forms
from .models import Contact
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CreateUserContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        exclude = ("user", "first_name", "last_name")


class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        )
