import email

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django import forms
from app.models import UserDetails, EmployerDetails

class AccountForm(UserChangeForm):

    password = None

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
        )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # First Name
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['first_name'].required = True
        self.fields['first_name'].error_messages['required'] = 'Please enter your first name.'
        # self.fields['username'].widget.attrs['class'] = '' # Add class here

        # Last Name
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['last_name'].required = True
        self.fields['last_name'].error_messages['required'] = 'Please enter your last name.'

        # Username
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].error_messages['required'] = 'Please enter your username.'

        # Email
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].required = True
        self.fields['email'].error_messages['required'] = 'Please enter your email.'

    def clean_username(self):
        username = self.cleaned_data["username"]

        if (User.objects
            .exclude(pk=self.instance.pk)
            .filter(username__iexact=username)
            .exists()
            ):
            
            raise forms.ValidationError("Username already exists.")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]

        if (User.objects
            .exclude(pk=self.instance.pk)
            .filter(email__iexact=email)
            .exists()):
            raise forms.ValidationError("Email already exists.")

        return email
    
    def clean(self):

        cleaned_data = super().clean()

        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if first_name == last_name:
            raise ValidationError(
                "First and Last Name cannot be same."
            )

        return cleaned_data

class UserDetailsForm(forms.ModelForm):
    
    
    class Meta:
        model = UserDetails
        fields = (
            "location",
            "mobile_no",
            "about_me",
            "skills",
            "education",
            "profile_img",
            "university",
            "priveus_job",
            "specialization",
            "interests",
            "gender",
        )
        labels = {
            "mobile_no":"Mobile Number",
            "priveus_job":"Previous Job",
            "about_me":"About Me",
        }
        
        error_messages = {
            "specialization": {
                "required": "Please enter your specialization.",
            },
            "education": {
                "required": "Please enter your education.",
            },
            "university": {
                "required": "Please enter your university.",
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        required_fields = [
            "first_name",
            "last_name",
            "email",
        ]

        for field in required_fields:
            self.fields[field].required = True
            
        placeholders = {
            "location": "Enter location",
            "mobile_no": "+92xxxxxxxxxx",
            "about_me": "Tell us about yourself",
            "skills": "Python, Django...",
            "education": "BS Computer Science",
            "university": "University",
            "priveus_job": "Previous Job",
            "specialization": "Backend Developer",
            "interests": "AI, ML...",
        }

        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs["placeholder"] = placeholder

        if "about_me" in self.fields:
            self.fields["about_me"].widget.attrs["rows"] = 4

        if "profile_img" in self.fields:
            self.fields["profile_img"].widget.attrs["accept"] = "image/*"

    def clean_mobile_no(self):
        mobile=self.cleaned_data.get("mobile_no")
        if mobile and len(mobile)<10:
            raise forms.ValidationError(
                "Enter a valid phone number."
            )
        return mobile

    def clean_specialization(self):
        specialization=self.cleaned_data.get(
            "specialization"
        )
        if specialization:
            specialization=specialization.strip()
        return specialization


class EmployerDetailsForm(forms.ModelForm):


    class Meta:
        model = EmployerDetails
        fields= ('__all__')        
        exclude =  ('employer','type') 

