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