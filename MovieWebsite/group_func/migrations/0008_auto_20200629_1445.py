# Generated by Django 3.0.7 on 2020-06-29 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_func', '0007_group_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouppost',
            name='views',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
