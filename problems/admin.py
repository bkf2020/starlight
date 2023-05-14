from django.contrib import admin
from .models import Hint, Insight, HintCluster, InsightCluster, OverallInsightCluster

# Register your models here.
admin.site.register(Hint)
admin.site.register(Insight)
admin.site.register(HintCluster)
admin.site.register(InsightCluster)
admin.site.register(OverallInsightCluster)
