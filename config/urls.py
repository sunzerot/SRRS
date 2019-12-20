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
from app.main.index import index, search
from app.mem.api import *
from app.room.api import *

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('login', login_page),
    path('join', join_page),
    path('myPage', my_page),
    path('rgtRoom', rgt_room),
    path('detailRoom', detail_room),

    url(r'^api/doc', get_swagger_view(title='Rest API Document')),          # restful api doc
    url(r'^api/main/search/', search),                                # 유저 회원가입
    url(r'^api/mem/members/$', member_list),                                # 유저 회원가입
    url(r'^api/mem/members/duplicate/', member_id_duplicate),               # 유저 아이디 중복체크
    url(r'^api/mem/members/login/$', member_login),                         # 유저 로그인(일반, 숙소등록 회원)
    url(r'^api/mem/members/logout/', member_logout),                        # 유저 로그아웃
    url(r'^api/mem/members/member/', member_info),                          # 유저 상세
    url(r'^api/mem/members/modify/', member_modify),                        # 유저 수정
# ------------------------------------------------------------------------------------------------------------
    url(r'^api/room/rooms/insert/', insert_room),                           # 유저 수정
    url(r'^api/room/rooms/reserve/', reserve_room),                           # 유저 수정
    url(r'^api/room/rooms/info/', reserve_info),                           # 유저 수정
    url(r'^api/room/rooms/noti/', reserve_noti),                           # 유저 수정
    url(r'^api/room/rooms/getNoti/', admin_get_noti),                           # 사용자 문의 가져오기
    url(r'^api/room/rooms/dtlNoti/', admin_dtl_noti),                           # 사용자 문의 상세 및 전송 가져오기






]
