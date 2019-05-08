from django.db import models
from django.contrib.auth.models import User


class MultiplyUserRank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    next_level_additional_experience = models.IntegerField(default=100)
