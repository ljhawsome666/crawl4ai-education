from django.urls import path
from .views import template_list

urlpatterns = [
    path('api/templates/', template_list),
]