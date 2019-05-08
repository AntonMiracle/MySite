from django.db import models
from django.contrib.auth.models import User


class MultiplyUserRank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    next_level = models.IntegerField(default=100)
