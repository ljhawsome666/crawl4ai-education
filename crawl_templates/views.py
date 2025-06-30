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
            'method': t.method
        }
        for t in templates
    ]
    return Response(data)