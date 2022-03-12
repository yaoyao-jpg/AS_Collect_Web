"""mysite1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from AS_Collect import views

urlpatterns = [
    #path('admin/', admin.site.urls),

    #主页面
    path('',views.main_page),

    # 乃宝B站专栏二创
    path('news/', views.news),

    #乃宝B站视频二创
    path('video/',views.video),

    #豆瓣文章
    path('douban/',views.douban),

]













