from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("username", "password")

    username = forms.RegexField(label="Username", max_length=30, regex=r'^[\w.@+-]+$',
                                help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only." )
                              
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class UserCreationForm(UserForm):
    password_confirm = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
                                help_text = "Must be same as above.")
    email = forms.EmailField(label="Email", max_length=75)
