from django.contrib import admin
from .models import CrawlTemplate

@admin.register(CrawlTemplate)
class CrawlTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    search_fields = ('name', 'category')