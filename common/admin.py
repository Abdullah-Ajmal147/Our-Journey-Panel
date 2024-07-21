from django.contrib import admin

from common.models import Support

# Register your models here.
# @admin.register(Support)
# class TicketAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'subject', 'status', 'created_at', 'updated_at']
#     list_filter = ['status', 'created_at', 'updated_at']
#     search_fields = ['subject', 'description', 'user__username']
#     ordering = ['-created_at']