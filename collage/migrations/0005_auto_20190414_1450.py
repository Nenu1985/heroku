# Generated by Django 2.1.7 on 2019-04-14 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collage', '0004_auto_20190414_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cutphoto',
            name='photo_src',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collage.Photo', unique=True),
        ),
    ]
