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


class RestaurantReview(BaseModel):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    text = models.TextField(max_length=500)
    rating = models.IntegerField(max_length=1)


#cannot extend RestaurantLike here because RestaurantLike is not abstract.
class RestaurantComment(BaseModel):
    user = models.ForeignKey(User)
    restaurant_review = models.ForeignKey(RestaurantReview)
    text = models.TextField(max_length=500)

class RestaurantVisits(BaseModel):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    visit_count = models.IntegerField(max_length=11)

class Team(BaseModel):
    name = models.CharField(max_length=100)
    
    
