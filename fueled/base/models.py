from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, blank=False, editable=False)
    updated = models.DateTimeField(auto_now=True, blank=False, editable=False)

    class Meta:
        abstract = True
