# Generated by Django 5.0.6 on 2024-06-21 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='country_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='customuser',
            name='ride_category',
            field=models.CharField(blank=True, choices=[('RideAc', 'RideAc'), ('Echo', 'Echo')], max_length=20),
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('admin', 'admin'), ('captain', 'captain'), ('customer', 'customer')], max_length=20),
        ),
    ]
