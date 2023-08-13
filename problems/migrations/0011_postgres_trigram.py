from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('problems', '0010_alter_problem_name'),
    ]
    operations = [TrigramExtension()]