# Generated by Django 5.0.6 on 2024-07-20 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_review_user_remove_support_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
