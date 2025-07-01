from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CrawlTemplate

@api_view(['GET'])
def template_list(request):
    templates = CrawlTemplate.objects.all().order_by('-created_at')
    data = [
        {
            'name': t.name,
            'category': t.category,
            'method': t.method,

            # 新增以下字段
            'url': t.url,
            'raw_keyword': t.keywords,
            'max_depth': t.max_depth,
            'include_external': t.include_external,
            'strategy': t.strategy
        }
        for t in templates
    ]
    return Response(data)
