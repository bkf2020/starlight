from django.contrib import admin
from .models import Hint, Insight, HintCluster, InsightCluster, OverallInsightCluster, Problem, Collection, ProblemInCollection

# Register your models here.
admin.site.register(Hint)
admin.site.register(Insight)
admin.site.register(HintCluster)
admin.site.register(InsightCluster)
admin.site.register(OverallInsightCluster)
admin.site.register(Problem)
admin.site.register(Collection)
admin.site.register(ProblemInCollection)
