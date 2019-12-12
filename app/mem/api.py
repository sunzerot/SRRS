from datetime import datetime
import hashlib
import os

from django import db
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework import serializers, status
import hashlib
import json
from rest_framework.response import Response

from app.sys.models import Member
from rest_framework.decorators import api_view


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


# 로그인 페이지
def login_page(request):
    return render(request, 'home/mem/login-page.html')


# 회원가입 페이지
def join_page(request):
    return render(request, 'home/mem/join-page.html')


# 마이페이지
def my_page(request):

    if 'user_email' not in request.session:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/login'))
    else:
        return render(request, 'home/mem/my-page.html')

# 아이디 중복 체크
@api_view(['GET'])
def member_id_duplicate(request):
    if request.method == 'GET':
        user_email = request.GET.get('user_email')
        member = Member.objects.filter(user_email=user_email)
        serializer = MemberSerializer(member, many=True)

        return Response(len(serializer.data))

#  아이디 등록
@api_view(['GET', 'POST'])
def member_list(request):
    if request.method == 'GET':
        member = Member.objects.all()
        serializer = MemberSerializer(member, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            post_data = request.data
            dump_data = json.dumps(post_data)
            data = json.loads(dump_data)
            data['user_pwd'] = hashlib.md5(data['user_pwd'].encode('utf-8')).hexdigest()
            serializer = MemberSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                resp_msg = u"회원가입이 완료됐습니다."
                return Response(resp_msg)
            resp_msg = u"회원가입에 문제가 생겼습니다. 잠시 후 다시 시도해주세요."
            return Response(resp_msg)
        except ZeroDivisionError as e:
            print(e)
            resp_msg = u"회원가입에 문제가 생겼습니다. 잠시 후 다시 시도해주세요."
            return Response(resp_msg)

@api_view(['POST'])
def member_login(request):
    resp_msg = ''  # 보낼 메시지 초기화
    if request.method == 'GET':
        resp_msg = u"'잘못된 접근입니다."
    elif request.method == 'POST':
        p = request.data
        dump_data = json.dumps(p)
        data = json.loads(dump_data)

        # 로그인 query
        cursor = db.connection.cursor()
        login_query = """
                  SELECT * 
                    FROM member
                   WHERE user_pwd = md5('%s') and user_email = '%s'
              """ % (data['user_pwd'], data['user_email'])

        cursor.execute(login_query)
        result = cursor.fetchone()

        if result is None:
            resp_msg = u"ID가 없거나, 비밀번호가 잘못되었습니다."
        else:

            try:
                resp_msg = u"success"
                request.session["user_email"] = result[2]
                request.session["user_name"] = result[1]
                request.session["user_phone"] = result[4]
                return Response(resp_msg)
            except Exception as e:
                print(e)

                resp_msg = u"로그인이 실패하였습니다."

    return HttpResponse(resp_msg)


# 유저 로그아웃
@api_view(["POST"])
def member_logout(request):
    resp_msg = ''
    if request.method == 'GET':
        resp_msg = u"'잘못된 접근입니다."
    elif request.method == 'POST':
        try:
            del request.session['user_email']
            resp_msg = u"success"
        except Exception as e:
            print(e)
            resp_msg = u"통신에 오류가 발생했습니다."

    return Response(resp_msg)


# 유저 상세
@api_view(["POST"])
def member_info(request):
    if request.method == 'GET':
        resp_msg = u"'잘못된 접근입니다."
        return Response(resp_msg)
    elif request.method == 'POST':
        post_data = request.data
        dump_data = json.dumps(post_data)
        data = json.loads(dump_data)
        cursor = db.connection.cursor()
        member_query = """
              SELECT user_email, user_name, user_hp
                FROM member
               WHERE user_email = '%s'
          """ % (data['user_email'])

        cursor.execute(member_query)
        rtn = cursor.fetchone()


        result = []
        keys = ('user_email', 'user_name', 'user_phone',)
        # for row in member_query:
        result.append(dict(zip(keys, rtn)))
        json_data = json.dumps(result)
        return HttpResponse(json_data, content_type="application/json")



# 유저 수정
@api_view(["POST"])
def member_modify(request):
    resp_msg = ''
    if request.method == 'GET':
        resp_msg = u"'잘못된 접근입니다."
    elif request.method == 'POST':
        post_data = request.data
        dump_data = json.dumps(post_data)
        data = json.loads(dump_data)
        cursor = db.connection.cursor()
        if data["user_pwd"] != "":
            update_pwd_query = """
                 UPDATE member
                 SET user_pwd = md5('%s')
                   , user_hp = '%s'
                   , user_name = '%s'
                 WHERE user_email = '%s'
             """ % (data['user_pwd'], data["user_phone"], data["user_name"], data["user_email"])
        else:
            update_pwd_query = """
                 UPDATE member
                 SET user_hp = '%s'
                   , user_name = '%s'
                 WHERE user_email = '%s'
             """ % (data['user_phone'], data["user_name"], data["user_email"])

        cursor.execute(update_pwd_query)
        resp_msg = u"success"

    return HttpResponse(resp_msg)