from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Schedule

# admin.site.register(CustomUser)
@admin.register(CustomUser)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'is_staff', 'role']
    list_filter = ('role', 'name')
    search_fields = ('email',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_time', 'end_time', 'route_start', 'route_end')
    search_fields = ('user__username', 'route_start', 'route_end')
    list_filter = ('user', 'start_time', 'end_time')