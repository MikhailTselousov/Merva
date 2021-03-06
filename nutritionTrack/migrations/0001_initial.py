# Generated by Django 3.0.7 on 2020-06-09 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('kcals', models.DecimalField(decimal_places=2, max_digits=5)),
                ('carbs', models.DecimalField(decimal_places=2, max_digits=5)),
                ('prot', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fat', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('login', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('kcals', models.DecimalField(decimal_places=2, max_digits=5)),
                ('carbs', models.DecimalField(decimal_places=2, max_digits=5)),
                ('prot', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fat', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutritionTrack.Date')),
                ('ingredient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nutritionTrack.Ingredient')),
            ],
        ),
        migrations.AddField(
            model_name='date',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutritionTrack.User'),
        ),
    ]
