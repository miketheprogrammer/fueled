from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from restaurants.models import Restaurant
# Create your models here.


class RestaurantLike(BaseModel):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)

class RestaurantThumbsDown(BaseModel):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)

#cannot extend RestaurantLike here because RestaurantLike is not abstract.
class RestaurantComment(BaseModel):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    comment = models.CharField(max_length=255)

class RestaurantVisits(BaseModel):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    visit_count = models.IntegerField(max_length=11)

class Team(BaseModel):
    name = models.CharField(max_length=100)
    
    
