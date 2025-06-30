from django.db import models

class CrawlTask(models.Model):
    STRATEGY_CHOICES = [
        ('bfs', 'BFS'),
        ('dfs', 'DFS'),
        ('bestfirst', '智能优先'),
    ]

    url = models.URLField(verbose_name="目标网址")
    keyword = models.CharField(max_length=255, verbose_name="关键词")
    max_depth = models.PositiveIntegerField(default=2, verbose_name="最大爬取深度")
    include_external = models.BooleanField(default=False, verbose_name="是否包含外部链接")
    strategy = models.CharField(
        max_length=20,
        choices=STRATEGY_CHOICES,
        default='bestfirst',
        verbose_name="爬取策略"
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', '待启动'),
            ('running', '爬取中'),
            ('completed', '已完成'),
            ('failed', '失败')
        ],
        default='pending',
        verbose_name="任务状态"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    # 新增字段，用于存储爬取进度百分比（0~100）
    progress = models.PositiveIntegerField(default=0, verbose_name="爬取进度")

    # 新增字段，用于存储爬取结果文件名
    filename = models.CharField(max_length=255, blank=True, default='', verbose_name="结果文件名")

    # 新增字段，用于存储结果文件的下载地址
    download_url = models.URLField(blank=True, default='', verbose_name="下载链接")

    def __str__(self):
        return f"[{self.get_status_display()}] {self.keyword} - {self.url}"


class CrawlResultShowcase(models.Model):
    url = models.URLField()
    keyword = models.CharField(max_length=255)
    content_preview = models.TextField()  # 内容摘要或片段
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.keyword} - {self.url}'
