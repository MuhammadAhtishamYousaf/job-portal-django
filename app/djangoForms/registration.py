from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 


# menually
# from django import forms 
# from..models import User

from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  

  
class BuiltinUserCreationForm(UserCreationForm):  
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={ 'placeholder': 'DFirst Name', 'class': ''}))
    # last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={ 'placeholder': ' Dspecialization', 'class': ''}))
    # username = forms.CharField(label='username', min_length=30, max_length=150)  
    email = forms.EmailField(widget=forms.EmailInput(attrs={ 'placeholder': 'DEmail', 'class': ''}))  
    # password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    # password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  

  
   
    class Meta:
        model = User
        fields = ['id','first_name','username','email','password1', 'password2']
        # fields = ('__all__')
        # exclude = ('id') 

    def __init__(self, *args, **kwargs):
        super(BuiltinUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'DUser Name'
        self.fields['username'].widget.attrs['class'] = ''
        self.fields['password1'].widget.attrs['placeholder'] = 'DPassword'
        self.fields['password1'].widget.attrs['class'] = ''  # Add class here
        self.fields['password2'].widget.attrs['placeholder'] = 'DConfirm Password'
        self.fields['password2'].widget.attrs['class'] = ''  # Add class here


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