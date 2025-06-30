from django.db import models

class CrawlTemplate(models.Model):
    name = models.CharField(max_length=100, verbose_name="网站名称")
    category = models.CharField(max_length=50, verbose_name="网站分类")
    method = models.TextField(verbose_name="爬取方法")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name