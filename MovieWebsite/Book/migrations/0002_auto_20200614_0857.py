# Generated by Django 3.0.5 on 2020-06-14 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='good',
        ),
        migrations.RemoveField(
            model_name='book',
            name='num',
        ),
        migrations.RemoveField(
            model_name='book',
            name='rate_num',
        ),
        migrations.RemoveField(
            model_name='book',
            name='sump',
        ),
        migrations.AlterField(
            model_name='book',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='pic',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
