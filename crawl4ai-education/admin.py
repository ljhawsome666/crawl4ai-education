from django.contrib import admin
from .models import ScrapeTask


@admin.register(ScrapeTask)
class ScrapeTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'keyword', 'status', 'created_at')
    search_fields = ('url', 'keyword')
    list_filter = ('status',)


@admin.register(CrawlResultShowcase)
class CrawlResultShowcaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'keyword', 'url', 'is_approved', 'created_at')
    search_fields = ('keyword', 'url')
    list_filter = ('is_approved',)
    list_editable = ('is_approved',)
