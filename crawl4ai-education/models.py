from django.db import models
from django.contrib.auth.models import User

class ScrapeTask(models.Model):
    STATUS_CHOICES = [
        ('pending', '等待中'),
        ('running', '运行中'),
        ('success', '成功'),
        ('failed', '失败'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    url = models.URLField(verbose_name="目标网址")
    keyword = models.CharField(max_length=100, blank=True, verbose_name="关键词")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="状态")
    result_file = models.FileField(upload_to='results/', blank=True, null=True, verbose_name="结果文件")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"{self.user.username} - {self.url[:30]} - {self.status}"
