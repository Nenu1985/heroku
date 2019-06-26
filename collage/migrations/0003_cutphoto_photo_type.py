# Generated by Django 2.2 on 2019-06-24 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collage', '0002_auto_20190624_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='cutphoto',
            name='photo_type',
            field=models.IntegerField(choices=[(0, 'Objs rounded with rect'), (128, 'Resized to 128'), (256, 'Resized to 256'), (1, 'cut')], default=1),
        ),
    ]