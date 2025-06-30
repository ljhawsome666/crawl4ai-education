from django.urls import path
from .views import api_create_task, api_list_tasks, api_task_detail, start_crawl_task,task_progress

urlpatterns = [
    path('create-task/', api_create_task),
    path('tasks/', api_list_tasks),
    path('tasks/<int:pk>/', api_task_detail),          # 新增任务详情接口
    path('tasks/<int:pk>/start/', start_crawl_task),
    path('tasks/<int:pk>/progress/', task_progress),
]
