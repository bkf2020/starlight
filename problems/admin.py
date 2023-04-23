from django.contrib import admin
from .models import Hint, Insight, HintCluster

# Register your models here.
admin.site.register(Hint)
admin.site.register(Insight)
admin.site.register(HintCluster)
