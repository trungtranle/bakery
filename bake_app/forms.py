from django import forms
from .models import UserProfileInfo
from django.contrib.auth.models import User

class UserFrom(forms.ModelForm):
    
    password = forms.CharField(widget = forms.PasswordInput())
    password_confirm = forms.CharField(widget = forms.PasswordInput())
    
    class Meta():
        model = User
        fields = ('username','email','password','first_name', 'last_name')
        
class UserProfileInfoForm(forms.ModelForm):
    picture = forms.ImageField(required = False)

    class Meta():
        model = UserProfileInfo
        exclude = ('user','paid')

