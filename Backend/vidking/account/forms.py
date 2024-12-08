from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import UserFiles

class UserRegistationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        
    def clean_user(self):
        username = self.cleaned_data.get('username')   
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is exists")
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is exists")
        return email

    
    
    def clean_password2(self):
        cd = self.cleaned_data
        password = cd.get('password')
        password2 = cd.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError("NOT")
        return password2

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserFileForm(forms.ModelForm):
    class Meta:
        model = UserFiles
        fields = ['file']