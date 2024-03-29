from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User
from accounts.models import UserProfile
from restaurants.models import Restaurant
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget = forms.TextInput(attrs={'class':'input-block-level', 'required':True})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class':'input-block-level', 'required':True})


class UserCreationForm(UserForm):
    class Meta:
        model = User
        fields = ("username", "password", "password_confirm",  "email")

    password_confirm = forms.CharField(label="Password confirmation", 
                                       widget=forms.PasswordInput(attrs={'class':'input-block-level', 'required':True}),
                                       help_text="Must be same as above.",
                                       required=True)



class UserEditForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password", "password_confirm" , "first_name","last_name","email")

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].widget = forms.TextInput(attrs={'class':'input-block-level'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'class':'input-block-level'})

class UserProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ("favorite_cuisine",)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['favorite_cuisine'].widget = forms.Select(attrs={'class':'input-block-level', "required":True}, choices=Restaurant.cuisine_type_choices)

        
        
