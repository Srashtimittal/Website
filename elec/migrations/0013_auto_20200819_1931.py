# Generated by Django 3.0.7 on 2020-08-19 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elec', '0012_auto_20200819_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='image',
            field=models.ImageField(default='', upload_to='static/elec'),
        ),
    ]
