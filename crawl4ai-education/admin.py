from django.contrib import admin
from .models import ScrapeTask

@admin.register(ScrapeTask)
class ScrapeTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'keyword', 'status', 'created_at')
    search_fields = ('url', 'keyword')
    list_filter = ('status',)
