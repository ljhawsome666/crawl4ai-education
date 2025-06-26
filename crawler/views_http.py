# crawler/views_http.py —— 提供用于 HTTP API 的视图函数
import json
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import os
from .views import run_crawler
from crawler.models import CrawlResultShowcase
from asgiref.sync import async_to_sync
from django.conf import settings


@csrf_exempt
def crawl_and_filter(request):
    if request.method != 'POST':
        return JsonResponse({'error': '仅支持POST请求'}, status=405)
    try:
        data = json.loads(request.body)
        url = data.get('url')
        keyword = data.get('keyword')
        if not url or not keyword:
            return JsonResponse({'error': '参数缺失'}, status=400)

        result = async_to_sync(run_crawler)(url, keyword)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def download_file(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'output_files', filename)
    if not os.path.exists(file_path):
        raise Http404("文件不存在")
    return FileResponse(open(file_path, 'rb'), content_type='text/markdown; charset=utf-8')


def list_showcases(request):
    data = CrawlResultShowcase.objects.all().order_by('-created_at')
    result = [{
        'url': item.url,
        'keyword': item.keyword,
        'content_preview': item.content_preview,
    } for item in data]
    return JsonResponse(result, safe=False)
