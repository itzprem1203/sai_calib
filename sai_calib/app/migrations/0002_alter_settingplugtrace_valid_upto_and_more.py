# Generated by Django 5.1.1 on 2024-09-21 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settingplugtrace',
            name='valid_upto',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='settingringtrace',
            name='valid_upto',
            field=models.CharField(max_length=50),
        ),
    ]
