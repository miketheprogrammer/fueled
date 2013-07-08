from django.db import models
from django.contrib.auth.models import User
from social.models import Team
from base.models import BaseModel
class TeamUser(BaseModel):
    user = models.OneToOneField(User)
    team = models.ForeignKey(Team)

