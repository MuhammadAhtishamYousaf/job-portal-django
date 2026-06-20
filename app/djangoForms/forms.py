# forms.py

from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError


class CustomPasswordResetForm(PasswordResetForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(label="Email", max_length=254)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        first_name = cleaned_data.get('first_name')
        email = cleaned_data.get('email')

        # Validate username and first name
        if username and first_name:
            try:
                user = User.objects.get(username=username, first_name=first_name,email=email)
                # Check if the user email matches the one provided in the form
                if user.email != cleaned_data.get('email'):
                    raise ValidationError("Email does not match the provided details.")
            except User.DoesNotExist:
                raise ValidationError("No user found with the provided username and first name.")
        
        return cleaned_data

  