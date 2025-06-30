import json
from threading import Thread
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from asgiref.sync import async_to_sync
from crawler.models import CrawlTask
from crawler.views import run_crawler  # 你异步爬虫主函数

@csrf_exempt
@require_http_methods(["POST"])
def api_create_task(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        url = data.get("url")
        raw_keyword = data.get("raw_keyword")
        max_depth = int(data.get("max_depth", 1))
        include_external = data.get("include_external", False)
        strategy = data.get("strategy", "bfs")

        if not url or not raw_keyword:
            return JsonResponse({"error": "URL 和关键词是必填项"}, status=400)

        task = CrawlTask.objects.create(
            url=url,
            keyword=raw_keyword,
            max_depth=max_depth,
            include_external=include_external,
            strategy=strategy,
            status="pending"
        )
        return JsonResponse({"message": "任务创建成功", "task_id": task.id}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def api_list_tasks(request):
    tasks = CrawlTask.objects.all().order_by('-created_at')
    data = [
        {
            "id": task.id,
            "url": task.url,
            "keyword": task.keyword,
            "max_depth": task.max_depth,
            "include_external": task.include_external,
            "strategy": task.strategy,
            "status": task.status,
            "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "progress": task.progress,
            "filename": task.filename,
            "download_url": task.download_url,
        }
        for task in tasks
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
@require_http_methods(["GET", "PUT"])
def api_task_detail(request, pk):
    task = get_object_or_404(CrawlTask, pk=pk)
    if request.method == "GET":
        data = {
            "id": task.id,
            "url": task.url,
            "keyword": task.keyword,
            "max_depth": task.max_depth,
            "include_external": task.include_external,
            "strategy": task.strategy,
            "status": task.status,
            "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "progress": task.progress,
            "filename": task.filename,
            "download_url": task.download_url,
        }
        return JsonResponse(data)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body.decode())
            task.url = data.get("url", task.url)
            task.keyword = data.get("keyword", task.keyword)
            task.max_depth = int(data.get("max_depth", task.max_depth))
            task.include_external = data.get("include_external", task.include_external)
            task.strategy = data.get("strategy", task.strategy)
            task.save()
            return JsonResponse({"message": "任务更新成功"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return HttpResponseNotAllowed(["GET", "PUT"])


def run_crawl_in_thread(task_id):
    task = CrawlTask.objects.get(pk=task_id)
    try:
        print("原始key", task.keyword)
        raw_keyword = task.keyword
        if isinstance(raw_keyword, list):
            raw_keyword = ','.join(raw_keyword)   # 转成字符串，逗号分隔

        result = async_to_sync(run_crawler)(
            url=task.url,
            raw_keyword=raw_keyword,
            max_depth=task.max_depth,
            include_external=task.include_external,
            strategy=task.strategy
        )
        task.status = 'completed'
        task.filename = result.get('filename', '')
        task.download_url = result.get('download_url', '')
        task.progress = 100
    except Exception as e:
        task.status = 'failed'
        task.progress = 0
        print(f"任务 {task_id} 爬取失败: {e}")
    task.save(update_fields=['status', 'filename', 'download_url', 'progress'])


@api_view(['POST'])
def start_crawl_task(request, pk):
    task = get_object_or_404(CrawlTask, pk=pk)

    if task.status == 'running':
        return Response({"detail": "任务正在运行中"}, status=400)

    task.status = 'running'
    task.progress = 0
    task.save(update_fields=['status', 'progress'])

    Thread(target=run_crawl_in_thread, args=(task.id,), daemon=True).start()

    return Response({"detail": "任务已启动"})


@api_view(['GET'])
def task_progress(request, pk):
    task = get_object_or_404(CrawlTask, pk=pk)
    data = {
        "status": task.status,
        "progress": getattr(task, "progress", 0),
        "filename": getattr(task, "filename", ""),
        "download_url": getattr(task, "download_url", ""),
    }
    return Response(data)
