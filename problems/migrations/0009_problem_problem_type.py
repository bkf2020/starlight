# Generated by Django 4.2.1 on 2023-07-31 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0008_overallinsightcluster'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='problem_type',
            field=models.CharField(default='', max_length=100),
        ),
    ]