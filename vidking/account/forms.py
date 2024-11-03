from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserRegistationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password
    
    def clean_password2(self):
        cd = self.cleaned_data
        password = cd.get('password')
        password2 = cd.get('password2')
        
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2