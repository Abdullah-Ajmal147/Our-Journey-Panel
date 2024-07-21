# Generated by Django 5.0.6 on 2024-07-20 21:32

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_review_support'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.RemoveField(
            model_name='support',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='orders',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='orders',
            name='id',
        ),
        migrations.AddField(
            model_name='orders',
            name='estimated_distance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='estimated_duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='orders',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='orders',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='fare',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('paypal', 'PayPal')], default='cash', max_length=50),
        ),
        migrations.AlterField(
            model_name='orders',
            name='ride_type',
            field=models.CharField(choices=[('ride_ac', 'Ride AC'), ('ride_mini', 'Ride Mini'), ('ride_x', 'Ride X')], default='ride_ac', max_length=50),
        ),
        migrations.AlterField(
            model_name='orders',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='orders',
            index=models.Index(fields=['user'], name='order_order_user_id_1f6479_idx'),
        ),
        migrations.AddIndex(
            model_name='orders',
            index=models.Index(fields=['created_at'], name='order_order_created_0fc9cd_idx'),
        ),
        migrations.AddIndex(
            model_name='orders',
            index=models.Index(fields=['status'], name='order_order_status_53ea90_idx'),
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.DeleteModel(
            name='Support',
        ),
    ]
