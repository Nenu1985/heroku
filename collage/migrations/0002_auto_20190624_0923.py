# Generated by Django 2.2 on 2019-06-24 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cutphoto',
            name='img_location',
            field=models.FilePathField(path='D:\\opencv\\heroku\\nenu1985\\media\\upload_async'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='img_location',
            field=models.FilePathField(path='D:\\opencv\\heroku\\nenu1985\\media\\upload_async'),
        ),
    ]