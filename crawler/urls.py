from django.urls import path
from .views import crawl_and_filter, download_file

urlpatterns = [
    path('crawl-filter/', crawl_and_filter, name='crawl_and_filter'),
    path('download/<str:filename>/', download_file, name='download_file'),
]
