from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from django import forms
from ..models import UserDetails

class UserChangeCustomForm(UserChangeForm):


    class Meta:
        model = User
        fields = ('first_name','username','email')
        # fields = ('__all__')
        # exclude = ('user','type') 

class FullUserDetailsForm(forms.ModelForm):


    class Meta:
        model = UserDetails
        fields= ('__all__')        
        exclude = ('user','type')
        
class UserDetailsForm (forms.ModelForm):      
    location = forms.CharField(max_length=255, widget=forms.TextInput(attrs={ 'placeholder': 'Dlocation', 'class': ''})  )
    mobile_no = forms.CharField(max_length=255,widget=forms.TextInput(attrs={ 'placeholder': 'Dmobile', 'class': ''}) )
    about_me = forms.CharField( widget=forms.Textarea(attrs={ 'placeholder': 'Dabout', 'class': ''}) )
    skills = forms.CharField(max_length=200, widget=forms.TextInput(attrs={ 'placeholder': 'Dskills', 'class': ''}) )
    # date = forms.CharField(max_length=100, widget=forms.TextInput(attrs={ 'placeholder': 'Djoining date', 'class': ''}) )
    education = forms.CharField(max_length=255, widget=forms.TextInput(attrs={ 'placeholder': 'Deducation', 'class': ''}) )
    profile_img = forms.ImageField ()
    university = forms.CharField(max_length =66, widget=forms.TextInput(attrs={ 'placeholder': 'Duniverstiy', 'class': ''}) )
    priveus_job = forms.CharField(max_length=70, widget=forms.TextInput(attrs={ 'placeholder': 'Dprivious job', 'class': ''}) )
    # projects = forms.CharField(max_length =200, widget=forms.Textarea(attrs={ 'placeholder': 'Dprojects', 'class': ''}) )
    specialization = forms.CharField(max_length =200, widget=forms.TextInput(attrs={ 'placeholder': 'Dspecialization', 'class': ''}) )
    interests = forms.CharField(max_length =200, widget=forms.TextInput(attrs={ 'placeholder': 'Dinterests', 'class': ''}) )
    gender = forms.CharField(max_length =200, widget=forms.TextInput(attrs={ 'placeholder': 'Dgender', 'class': ''}) )
    type = forms.IntegerField ()
    
    class Meta:
        model = UserDetails
        # fields = ('location','mobile_no','about_me','skills','','about_me',)
        fields = ('__all__')
       


from django import forms
from ..models import EmployerDetails

class EmployerChangeCustomForm(UserChangeForm):


    class Meta:
        model = User
        fields = ('first_name','username','email')
        # fields = ('__all__')
        # exclude = ('user','type') 

class FullEmployerDetailsForm(forms.ModelForm):


    class Meta:
        model = EmployerDetails
        fields= ('__all__')        
        exclude =  ('employer','type') 

class EmployerDetailsForm (forms.ModelForm):      
    company_logo=forms.ImageField()
    industry = forms.CharField(max_length=255, widget=forms.TextInput(attrs={ 'placeholder': 'Dindustry', 'class': ''})  )
    company = forms.CharField(max_length=255,widget=forms.TextInput(attrs={ 'placeholder': 'Dcompany', 'class': ''}) )
    contact_no = forms.CharField( widget=forms.Textarea(attrs={ 'placeholder': 'Dcontact_no', 'class': ''}) )
    location = forms.CharField(max_length=200, widget=forms.TextInput(attrs={ 'placeholder': 'Dlocation', 'class': ''}) )

    class Meta:
        model = EmployerDetails
        # fields = ('location','mobile_no','about_me','skills','','about_me',)
        fields = ('__all__')
