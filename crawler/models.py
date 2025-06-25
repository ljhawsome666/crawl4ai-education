# crawler/models.py
from django.db import models

class CrawlResultShowcase(models.Model):
    url = models.URLField()
    keyword = models.CharField(max_length=255)
    content_preview = models.TextField()  # 内容摘要或片段
    is_approved = models.BooleanField(default=False)  # 管理员审核通过
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.keyword} - {self.url}'
