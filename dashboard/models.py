from django.db import models

class CrawlTask(models.Model):
    STATUS_CHOICES = [
        ('pending', '待启动'),
        ('running', '进行中'),
        ('completed', '已完成'),
    ]
    url = models.URLField()
    keyword = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.status}] {self.keyword} - {self.url}"
