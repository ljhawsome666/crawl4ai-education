# crawler/views_crawl.py

from asgiref.sync import async_to_sync
from .views import run_crawler  # 从 crawler/views.py 引入异步主函数

# ✅ 提供给外部 app（如 dashboard）调用的同步封装
def crawl_and_filter_sync(url: str, keyword: str):
    return async_to_sync(run_crawler)(url, keyword)
