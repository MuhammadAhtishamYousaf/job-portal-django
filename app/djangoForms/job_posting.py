from django import forms
from ..models import JobPosting
from django.contrib import messages

class JobPostingForm (forms.ModelForm):                                          
    job_title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={ 'placeholder': 'Djobtitle', 'class': ''}) )
    job_location = forms.CharField(max_length=255,widget=forms.TextInput(attrs={ 'placeholder': 'Djob location', 'class': ''}))
    job_description = forms.CharField( max_length = 1000,widget=forms.Textarea(attrs={ 'placeholder': 'Djob description', 'class': ''}) )
    skills_required = forms.CharField(max_length=200, widget=forms.TextInput(attrs={ 'placeholder': 'Dskill required', 'class': ''}))
    posting_date = forms.CharField(widget=forms.DateInput(attrs={ 'placeholder': 'D date', 'class': ''}) )
    salary = forms.CharField(max_length=255,widget=forms.TextInput(attrs={ 'placeholder': 'Dsalary', 'class': ''}))
   #  company_logo = forms.ImageField(   )
    industry = forms.CharField(max_length =66,widget=forms.TextInput(attrs={ 'placeholder': 'Dindustry', 'class': ''}))
    education = forms.CharField(max_length=70,widget=forms.TextInput(attrs={ 'placeholder': 'D education', 'class': ''}))
    experience_required = forms.CharField(max_length =200,widget=forms.TextInput(attrs={ 'placeholder': 'Dexperience required', 'class': ''}))
    gender = forms.CharField(max_length =200,widget=forms.TextInput(attrs={ 'placeholder': 'Dgender', 'class': ''}))
    company_name = forms.CharField(max_length =200,widget=forms.TextInput(attrs={ 'placeholder': 'Dcompany name', 'class': ''}))
    name = forms.CharField(max_length =200,widget=forms.TextInput(attrs={ 'placeholder': 'Dname', 'class': ''}))
    mobile_no = forms.CharField(max_length =200,widget=forms.NumberInput(attrs={ 'placeholder': 'D No#', 'class': ''}))
    email  = forms.EmailField(max_length =200,widget=forms.EmailInput(attrs={ 'placeholder': 'Demail', 'class': ''}))

    class Meta:
       model = JobPosting
       fields = ('__all__')

    # def clean_email(self):
    #     # Check if the email is already registered
    #     email = self.cleaned_data.get('email')
    #     if CustomUser.objects.filter(email=email).exists():
    #         messages.error(request="This email is already registered.")
    #     return email

    # def clean_username(self):
    #     # Check if the username is already taken
    #     username = self.cleaned_data.get('username')
    #     if CustomUser.objects.filter(username=username).exists():
    #         raise forms.ValidationError("This username is already taken.")
    #     return username

    # def clean_password2(self):
    #     # Check if the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords do not match")
    #     return password2

    # def save(self, commit=True):
    #      # Save the provided password in hashed format
    #      user = super().save(commit=False)
    #      user.email = self.cleaned_data["email"]
    #      if commit:
    #          user.save()
    #      return user

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if len(username) < 4:
    #         raise forms.ValidationError("Username must be at least 4 characters long.")
    #     return username

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     # Add email validation logic here if needed
    #     return email

    # def clean_password1(self):
    #     password1 = self.cleaned_data.get('password1')
    #     # Add password1 validation logic here if needed
    #     return password1

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #     if password1 != password2:
    #         raise forms.ValidationError("Passwords do not match.")
    #     return password2

    # def clean_first_name(self):
    #     first_name = self.cleaned_data.get('first_name')
    #     # Add first name validation logic here if needed
    #     return first_name