from django.db import models
from django.utils import timezone
from problems.models import Problem

# Create your models here.

STATUS_CHOICES = (
    ('NS', 'Not started'),
    ('IP', 'In progress'),
    ('NHS', 'Needed help to solve'),
    ('SO', 'Solved')
)

class JournalProblem(models.Model):
    problem = models.ForeignKey(Problem, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NS")
    username = models.CharField(max_length=150, default="")
    time_created = models.DateTimeField(default=timezone.now)

FILTER_CHOICES = (
    ('entire', 'entire'),
    ('week', 'week'),
    ('month', 'month'),
    ('year', 'year')
)

class JournalConfig(models.Model):
    username = models.CharField(max_length=150, default="")
    type_filter = models.CharField(max_length=6, choices=FILTER_CHOICES, default="entire")
    desired_year = models.IntegerField(default=2023)
    desired_month = models.IntegerField(default=1)
    desired_week = models.IntegerField(default=1)
    desired_page = models.IntegerField(default=1)