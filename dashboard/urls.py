from django.urls import path
from .views import api_create_task
from .views import api_list_tasks

urlpatterns = [
    path('create-task/', api_create_task),
    path("tasks/", api_list_tasks),
]
