from django.db import models
from django.db.models.signals import post_delete
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
    hint = models.ForeignKey(Hint, null=True, on_delete=models.CASCADE)
    cluster_id = models.IntegerField(default=-1)
    first = models.BooleanField(default=False)

class InsightCluster(models.Model):
    problem_id = models.IntegerField(default=-1)
    insight = models.ForeignKey(Insight, null=True, on_delete=models.CASCADE)
    cluster_id = models.IntegerField(default=-1)
    first = models.BooleanField(default=False)

def update_first_hint_cluster(sender, **kwargs):
    new_first = HintCluster.objects.first()
    new_first.first = True
    new_first.save()

def update_first_insight_cluster(sender, **kwargs):
    new_first = InsightCluster.objects.first()
    new_first.first = True
    new_first.save()

post_delete.connect(
    update_first_hint_cluster, sender=Hint
)
post_delete.connect(
    update_first_insight_cluster, sender=Insight
)