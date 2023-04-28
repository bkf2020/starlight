# Generated by Django 4.1.7 on 2023-04-28 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0005_remove_hintcluster_hint_id_hintcluster_hint'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsightCluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_id', models.IntegerField(default=-1)),
                ('cluster_id', models.IntegerField(default=-1)),
                ('first', models.BooleanField(default=False)),
                ('insight', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='problems.hint')),
            ],
        ),
    ]