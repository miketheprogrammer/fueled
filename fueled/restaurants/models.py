from django.db import models
from base.models import BaseModel
# Create your models here.

class Restaurant(BaseModel):
    cuisine_type_choices = (
        ('american', 'American'),
        ('chinese', 'Chinese'),
        ('french', 'French'),
        ('fusion', 'Fusion'),
    )

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    cuisine_type = models.CharField(max_length=255, choices=cuisine_type_choices)
    
