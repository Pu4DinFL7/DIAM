# Generated by Django 4.2.1 on 2023-05-10 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games_hub_app', '0002_image_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='description',
            field=models.CharField(max_length=20000),
        ),
    ]
