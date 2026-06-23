from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 


# menually
# from django import forms 
# from..models import User

from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  

  
class BuiltinUserCreationForm(UserCreationForm):  
    #we can also define fields here to add some widgts, extra validation, and checks
    
    # first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={ 'placeholder': 'First Name', 'class': ''}))
    # last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={ 'placeholder': ' specialization', 'class': ''}))
    # username = forms.CharField(label='username', min_length=30, max_length=150)  
    # email = forms.EmailField(widget=forms.EmailInput(attrs={ 'placeholder': 'Email', 'class': ''}))  
    # password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    # password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  

    spacialization = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Specialization'}),
    )
   
    class Meta:
        model = User
        # fields = ['first_name', 'last_name', 'username','email','password1', 'password2']
        fields = ('__all__')
        exclude = ('id',) 

    def __init__(self, *args, **kwargs):
        super(BuiltinUserCreationForm, self).__init__(*args, **kwargs)

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

        # Password
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].error_messages['required'] = 'Please create a password.'
        self.fields['password1'].help_text = 'Password does not contain any word from your name,username and email.'
        
        # Confirm Password
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].error_messages['required'] = 'Please confirm your password.'
        
    def clean_specialization(self):
        specialization = self.cleaned_data.get('specialization', '').strip()
        if not specialization:
            raise ValidationError('Specialization is required.')
        return specialization
    
    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
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

class BuiltinEmployerCreationForm(UserCreationForm):  
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={ 'placeholder': 'DFirst Name', 'class': ''}))
    # last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={ 'placeholder': ' Dspecialization', 'class': ''}))
    # username = forms.CharField(label='username', min_length=30, max_length=150)  
    email = forms.EmailField(widget=forms.EmailInput(attrs={ 'placeholder': 'DEmail', 'class': ''}))  



    class Meta:
        model = User
        fields = ['id','first_name','username','email','password1','password2' ]


    def __init__(self, *args, **kwargs):
        super(BuiltinEmployerCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'DUser Name'
        self.fields['password1'].widget.attrs['placeholder'] = 'DPassword'
        self.fields['password2'].widget.attrs['placeholder'] = 'DConfirm Password'

    # def username_clean(self):  
    #     username = self.cleaned_data['username'].lower()  
    #     new = User.objects.filter(username = username)  
    #     if new.count():  
    #         raise ValidationError("User Already Exist")  
    #     return username  
  
    # def email_clean(self):  
    #     email = self.cleaned_data['email'].lower()  
    #     new = User.objects.filter(email=email)  
    #     if new.count():  
    #         raise ValidationError(" Email Already Exist")  
    #     return email  
  
    # def clean_password2(self):  
    #     password1 = self.cleaned_data['password1']  
    #     password2 = self.cleaned_data['password2']  
  
    #     if password1 and password2 and password1 != password2:  
    #         raise ValidationError("Password don't match")  
    #     return password2  
  
    # def save(self, commit = True):  
    #     user = User.objects.create_user(
    #         self.cleaned_data['first_name'],  
    #         self.cleaned_data['username'],  
    #         self.cleaned_data['email'],  
    #         self.cleaned_data['password1']  
    #     )  
    #     return user  
