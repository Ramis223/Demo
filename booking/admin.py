from django.contrib import admin
from .models import Hall, Booking

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'capacity']
    list_editable = ['name', 'capacity']
    search_fields = ['name']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'hall', 'date', 'payment', 'status', 'created_at']
    list_filter = ['status', 'payment', 'hall', 'date']
    search_fields = ['user__username', 'hall__name']
    list_editable = ['status']
    date_hierarchy = 'date'
    list_per_page = 10
    
    actions = ['mark_as_scheduled', 'mark_as_completed']
    
    def mark_as_scheduled(self, request, queryset):
        queryset.update(status='scheduled')
    mark_as_scheduled.short_description = 'Назначить мероприятие'
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = 'Завершить мероприятие'