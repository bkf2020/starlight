from django.db import models

STATUS_CHOICES = (
    ('NP', "Not Processed"),
    ('CU', "Currently Processing"),
    ('FI', "Finished Processing")
)

class ImportStatus(models.Model):
    username = models.CharField(max_length=150, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NP")