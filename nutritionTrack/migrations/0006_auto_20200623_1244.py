# Generated by Django 3.0.7 on 2020-06-23 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutritionTrack', '0005_auto_20200623_1242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='fat',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='prot',
        ),
    ]