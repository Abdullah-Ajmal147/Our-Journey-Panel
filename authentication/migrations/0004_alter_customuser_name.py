# Generated by Django 5.0.6 on 2024-06-25 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
