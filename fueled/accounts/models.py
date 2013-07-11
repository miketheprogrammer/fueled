from django.db import models
from django.contrib.auth.models import User
from social.models import Team
from base.models import BaseModel
from restaurants.models import Restaurant
from django.db.models.signals import post_save

class TeamUser(BaseModel):
    user = models.OneToOneField(User)
    team = models.ForeignKey(Team)

class UserProfile(BaseModel):
    user = models.OneToOneField(User, related_name="profile")
    favorite_cuisine = models.CharField(max_length=255, choices=Restaurant.cuisine_type_choices)

