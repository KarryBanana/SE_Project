# Generated by Django 3.0.7 on 2020-06-29 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group_func', '0009_auto_20200629_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='views',
        ),
        migrations.RemoveField(
            model_name='grouppost',
            name='views',
        ),
    ]
