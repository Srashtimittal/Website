# Generated by Django 3.0.7 on 2020-07-26 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elec', '0009_auto_20200726_1728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='good',
            name='desc',
        ),
        migrations.RemoveField(
            model_name='good',
            name='sub_category1',
        ),
    ]
