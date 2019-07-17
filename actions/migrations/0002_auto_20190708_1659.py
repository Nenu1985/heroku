# Generated by Django 2.2 on 2019-07-08 13:59

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import images.models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='target_ct',
            field=models.ForeignKey(blank=True, limit_choices_to=(images.models.Image, django.contrib.auth.models.User), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_obj', to='contenttypes.ContentType'),
        ),
    ]