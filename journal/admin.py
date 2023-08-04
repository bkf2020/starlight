from django.contrib import admin
from .models import JournalProblem, JournalConfig

# Register your models here.
admin.site.register(JournalProblem)
admin.site.register(JournalConfig)
