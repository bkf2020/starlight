from django.db import models
from django.db.models.signals import post_save, post_delete
from django.core.validators import MinLengthValidator

class Problem(models.Model):
    name = models.CharField(max_length=200)
    link = models.URLField(default="")
    problem_type = models.CharField(max_length=100, default="")

class Collection(models.Model):
    name = models.CharField(max_length=200, default="")
    slug = models.SlugField()

class ProblemInCollection(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

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

class OverallInsightCluster(models.Model):
    problem_id = models.IntegerField(default=-1)
    insight = models.ForeignKey(Insight, null=True, on_delete=models.CASCADE)
    cluster_id_overall = models.IntegerField(default=-1)
    cluster_id_in_problem = models.IntegerField(default=-1)

def update_first_hint_cluster(sender, **kwargs):
    problem_id = kwargs.get('instance').problem_id
    cluster_id = kwargs.get('instance').cluster_id
    new_first = HintCluster.objects.filter(
        problem_id=problem_id,
        cluster_id=cluster_id
    )
    if(new_first.count() > 0):
        new_first = new_first.first()
        new_first.first = True
        new_first.save()

def update_first_insight_cluster(sender, **kwargs):
    problem_id = kwargs.get('instance').problem_id
    cluster_id = kwargs.get('instance').cluster_id
    new_first = InsightCluster.objects.filter(
        problem_id=problem_id,
        cluster_id=cluster_id
    )
    if(new_first.count() > 0):
        new_first = new_first.first()
        new_first.first = True
        new_first.save()

from journal.models import JournalProblem
def create_journal_problem(sender, **kwargs):
    problem_id = kwargs.get('instance').problem_id
    username = kwargs.get('instance').username
    if JournalProblem.objects.filter(problem_id=problem_id, username=username).count() == 0:
        new_journal_problem = JournalProblem(
            problem=Problem.objects.get(id=problem_id),
            username=username
        )
        new_journal_problem.save()

post_delete.connect(
    update_first_hint_cluster, sender=HintCluster
)
post_delete.connect(
    update_first_insight_cluster, sender=InsightCluster
)
post_save.connect(
    create_journal_problem, sender=Insight
)
