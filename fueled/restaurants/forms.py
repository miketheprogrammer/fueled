from django import forms
from django.forms import ModelForm, Form
from restaurants.models import Restaurant

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant

        fields = ("name", "address", "latitude", "longitude", "phone", "cuisine_type")

    def __init__(self, *args, **kwargs):
        super(RestaurantForm, self).__init__(*args, **kwargs)

        for k, field in self.fields.items():
            field.widget = forms.TextInput(attrs={'class':'input-block-level', "required":True})

        self.fields['cuisine_type'].widget = forms.Select(attrs={'class':'input-block-level', "required":True}, choices=Restaurant.cuisine_type_choices)

