# Generated by Django 4.1.7 on 2023-04-03 05:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_hint'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300, validators=[django.core.validators.MinLengthValidator(8)])),
                ('problem_id', models.IntegerField(default=-1)),
                ('username', models.CharField(default='', max_length=128)),
            ],
        ),
        migrations.RenameField(
            model_name='hint',
            old_name='name',
            new_name='text',
        ),
    ]