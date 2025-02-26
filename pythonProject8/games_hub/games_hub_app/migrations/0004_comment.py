# Generated by Django 4.2.1 on 2023-05-11 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games_hub_app', '0003_image_name_alter_image_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=20000)),
                ('comment_data', models.DateTimeField(verbose_name='Comment Date')),
            ],
        ),
    ]
