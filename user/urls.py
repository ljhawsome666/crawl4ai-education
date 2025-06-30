from django.urls import path
from .views import RegisterView, LoginView, UserProfileView

from . import views

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', UserProfileView.as_view()),  # 👈 当前登录用户信息接口

]