from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# 将自定义用户模型注册到后台
admin.site.register(CustomUser, UserAdmin)
