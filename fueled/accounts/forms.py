from django.forms import ModelForm, Form
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
