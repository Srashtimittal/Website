# Generated by Django 3.0.7 on 2020-07-13 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elec', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='desc',
        ),
        migrations.AlterField(
            model_name='item',
            name='it_name',
            field=models.CharField(max_length=500),
        ),
    ]
