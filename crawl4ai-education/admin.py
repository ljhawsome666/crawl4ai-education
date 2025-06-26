from django.contrib import admin
from crawler.models import CrawlResultShowcase
from .models import ScrapeTask


@admin.register(ScrapeTask)
class ScrapeTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'keyword', 'status', 'created_at')
    search_fields = ('url', 'keyword')
    list_filter = ('status',)


@admin.register(CrawlResultShowcase)
class ShowcaseAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'url', 'created_at')  # ✅ 删除 is_approved
    search_fields = ('keyword', 'url', 'content_preview')

