# Generated by Django 5.2.4 on 2025-07-21 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='word',
            field=models.CharField(default='', max_length=5),
        ),
    ]
