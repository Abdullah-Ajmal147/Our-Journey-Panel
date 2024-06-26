# admin.py
from django.contrib import admin
from .models import PaymentHistory

class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('payment_intent_id', 'amount', 'currency', 'status', 'email', 'created_at', 'updated_at')
    search_fields = ('payment_intent_id', 'email')
    list_filter = ('status', 'currency', 'created_at')

admin.site.register(PaymentHistory, PaymentHistoryAdmin)
