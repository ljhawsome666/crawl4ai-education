# crawl_templates/models.py

from django.db import models

class CrawlTemplate(models.Model):
    name = models.CharField(max_length=100, verbose_name="网站名称")
    category = models.CharField(max_length=50, verbose_name="网站分类")
    method = models.TextField(verbose_name="爬取方法")

    url = models.URLField(verbose_name="目标 URL")
    keywords = models.TextField(verbose_name="关键词", help_text="多个关键词用逗号分隔")
    max_depth = models.PositiveIntegerField(default=1, verbose_name="最大深度")
    include_external = models.BooleanField(default=False, verbose_name="包含外链")
    strategy = models.CharField(
        max_length=20,
        choices=[("bfs", "BFS"), ("dfs", "DFS"), ("bestfirst", "BestFirst")],
        default="bfs",
        verbose_name="爬取策略"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
