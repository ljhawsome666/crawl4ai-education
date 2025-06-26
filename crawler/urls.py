# crawler/urls.py
from django.urls import path
from .views_http import crawl_and_filter, download_file, list_showcases

urlpatterns = [
    path('crawl-filter/', crawl_and_filter, name='crawl-filter'),              # POST 爬取并筛选
    path('download/<str:filename>/', download_file, name='download-file'),     # GET 下载爬取结果
    path('showcase/', list_showcases, name='crawl-showcase'),                  # GET 获取历史结果
]
