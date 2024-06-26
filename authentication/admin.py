from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# admin.site.register(CustomUser)
@admin.register(CustomUser)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'is_staff', 'role']
    list_filter = ('role', 'name')
    search_fields = ('email',)