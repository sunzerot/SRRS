import hashlib
import os

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
