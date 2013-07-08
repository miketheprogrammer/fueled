from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from restaurants.models import Restaurant
# Create your models here.


class RestaurantLike(BaseModel):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)

#cannot extend RestaurantLike here because RestaurantLike is not abstract.
class RestaurantComment(BaseModel):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    comment = models.CharField(max_length=255)


class Team(BaseModel):
    name = models.CharField(max_length=100)
    
    