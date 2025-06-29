from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from crawler.models import CrawlTask
import json

@csrf_exempt
def api_create_task(request):
    if request.method == "POST":
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
                status="未启动"
            )
            return JsonResponse({"message": "任务创建成功", "task_id": task.id}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "仅支持 POST"}, status=405)

def api_list_tasks(request):
    tasks = CrawlTask.objects.all().order_by('-created_at')  # 最新优先
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
        }
        for task in tasks
    ]
    return JsonResponse(data, safe=False)