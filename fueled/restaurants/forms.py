from django import forms
from django.forms import ModelForm, Form
from restaurants.models import Restaurant

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant


