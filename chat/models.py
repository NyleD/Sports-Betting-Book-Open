from django.db import models
from betting.models import Group

class Room(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True, default=None)

    def __str__(self):
        return self.name
        

    