from django.contrib import admin
from .models import Orders, Location, Support

@admin.register(Support)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subject', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['subject', 'description', 'user__username']
    ordering = ['-created_at']

class LocationAdmin(admin.ModelAdmin):
    list_display = ('address', 'latitude', 'longitude')
    search_fields = ('address',)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_location', 'to_location', 'ride_type', 'fare', 'payment_method', 'created_at', 'updated_at')
    search_fields = ('user__username', 'from_location__address', 'to_location__address')
    list_filter = ('ride_type', 'payment_method', 'created_at', 'updated_at')
    autocomplete_fields = ('user', 'from_location', 'to_location')

admin.site.register(Location, LocationAdmin)
admin.site.register(Orders, OrdersAdmin)