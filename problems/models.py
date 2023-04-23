from django.db import models
from django.core.validators import MinLengthValidator

class Problem(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField(default="")

class Hint(models.Model):
    text = models.CharField(max_length=300, validators=[MinLengthValidator(8)])
    problem_id = models.IntegerField(default=-1)
    username = models.CharField(default="", max_length=128)

class Insight(models.Model):
    text = models.CharField(max_length=300, validators=[MinLengthValidator(8)])
    problem_id = models.IntegerField(default=-1)
    username = models.CharField(default="", max_length=128)

class HintCluster(models.Model):
    problem_id = models.IntegerField(default=-1)
    hint_id = models.IntegerField(default=-1)
    cluster_id = models.IntegerField(default=-1)
    first = models.BooleanField(default=False)