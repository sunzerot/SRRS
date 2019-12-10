"""sejongTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from app.main.index import index
from app.mem.api import *

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('login', login_page),
    path('join', join_page),

    url(r'^api/doc', get_swagger_view(title='Rest API Document')),          # restful api doc
    url(r'^api/mem/members/$', member_list),                                # 유저 회원가입
    url(r'^api/mem/members/duplicate/', member_id_duplicate),               # 유저 아이디 중복체크


]
