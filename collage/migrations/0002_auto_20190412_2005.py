# Generated by Django 2.1.7 on 2019-04-12 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collage',
            name='photo_size',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='collage.PhotoSize'),
        ),
        migrations.AlterField(
            model_name='photosize',
            name='size',
            field=models.IntegerField(default=128),
        ),
    ]
