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

def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.get_profile()
    except UserProfile.DoesNotExist as e:
        print e
        UserProfile.objects.create(user=instance, favorite_cuisine="fusion")
post_save.connect(create_user_profile, sender=User)
