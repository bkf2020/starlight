# Generated by Django 4.2.4 on 2023-08-30 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0012_collection_problemincollection'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]