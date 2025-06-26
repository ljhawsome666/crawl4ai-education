from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CrawlTask
from .serializers import CrawlTaskSerializer
from threading import Thread
from crawler.views_crawl import crawl_and_filter_sync  # 👈 你要封装的同步爬虫调用逻辑


class CrawlTaskViewSet(viewsets.ModelViewSet):
    queryset = CrawlTask.objects.all().order_by('-created_at')
    serializer_class = CrawlTaskSerializer

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        task = self.get_object()

        def run_task():
            try:
                task.status = 'running'
                task.save()

                # ✅ 调用爬虫逻辑（同步调用，但运行在线程中）
                crawl_and_filter_sync(task.url, task.keyword)

                task.status = 'completed'
                task.save()
            except Exception as e:
                task.status = 'failed'
                task.save()
                print(f"任务执行失败: {e}")

        # ✅ 用线程后台运行，不阻塞主线程
        Thread(target=run_task).start()

        return Response({'message': f'任务 "{task.keyword}" 已启动（后台执行）'})
