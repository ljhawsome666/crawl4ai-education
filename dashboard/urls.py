from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CrawlTaskViewSet

router = DefaultRouter()
router.register(r'', CrawlTaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]
