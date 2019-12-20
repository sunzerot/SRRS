from datetime import datetime
import hashlib
import os
from io import BytesIO

from PIL import Image

from django import db
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework import serializers, status
import hashlib
import json
from rest_framework.response import Response

from app.sys.models import Member, Rooms
from rest_framework.decorators import api_view



from config import settings


def rgt_room(request):

    if 'user_level' not in request.session:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return render(request, 'home/room/roomRgt.html')

#  숙소 등록
@api_view(['GET', 'POST'])
def insert_room(request):
    if request.method == 'GET':
        resp_msg = u"quit"
        return Response(resp_msg)

    elif request.method == 'POST':
        try:
            post_data = request.data
            user_seq = Member.objects.get(user_email=post_data["email"])
            seq_no = user_seq.seq_no

            test11 = ""
            test22 = ""
            test33 = ""
            test44 = ""
            test55 = ""
            test66 = ""
            test77 = ""

            oneBed = post_data["oneBed"]
            twoBed = post_data["twoBed"]
            threeBed = post_data["threeBed"]
            living = post_data["living"]
            rest = post_data["rest"]
            rest2 = post_data["rest2"]
            kit = post_data["kit"]

            if oneBed is not '':
                test = file_input(oneBed, seq_no)
                test11 = "static/img/rooms/" + str(seq_no) + "/" + test
            if twoBed is not '':
                test2 = file_input(twoBed, seq_no)
                test22 = "static/img/rooms/" + str(seq_no) + "/" + test2

            if threeBed is not '':
                test3 = file_input(threeBed, seq_no)
                test33 = "static/img/rooms/" + str(seq_no) + "/" + test3

            if living is not '':
                test4 = file_input(living, seq_no)
                test44 = "static/img/rooms/" + str(seq_no) + "/" + test4

            if rest is not '':
                test5 = file_input(rest, seq_no)
                test55 = "static/img/rooms/" + str(seq_no) + "/" + test5

            if rest2 is not '':
                test6 = file_input(rest2, seq_no)
                test66 = "static/img/rooms/" + str(seq_no) + "/" + test6

            if kit is not '':
                test7 = file_input(kit, seq_no)
                test77 = "static/img/rooms/" + str(seq_no) + "/" + test7

            cursor = db.connection.cursor()
            login_query = """
                              INSERT INTO rooms (rm_nm, rm_addr, rm_type, rm_adult, rm_mon_max_pay,
                              rm_sun_max_pay, rm_max_pay, rm_max_day, rm_chk_in_time, rm_chk_out_time, rm_room1_path, rm_room2_path,
                              rm_room3_path, rm_cik_path, rm_tol1_path, rm_tol2_path, rm_living_path, rm_is_use, rm_email, rm_phone)
                              values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 'Y', '%s', '%s')
                          """ % (post_data['rmNm'], post_data['addr'], post_data['rmType'], post_data['personal'], post_data['monPay'],
                                 post_data['sunPay'], post_data['maxPay'], post_data['day'], post_data['chkIn'], post_data['chkOut'],
                                 test11, test22, test33, test44, test55, test66, test77, post_data["email"], post_data["phone"])

            cursor.execute(login_query)

            resp_msg = u'success'
            return Response(resp_msg)
        except ZeroDivisionError as e:
            print(e)
            resp_msg = u"fail"
            return Response(resp_msg)


@api_view(['GET', 'POST'])
def detail_room(request):

    post_data = request.data
    content = Rooms.objects.filter(seq_no=post_data["seqNo"])
    return render(request, 'home/room/roomDetail.html', {'result': content})



@api_view(['GET', 'POST'])
def reserve_room(request):
    post_data = request.data

    cursor = db.connection.cursor()
    login_query = """
                                  INSERT INTO reservation (rm_no, user_id, chk_in_time, chk_out_time)
                                  values ('%s', '%s', '%s', '%s')
                              """ % (
                                post_data['seqNo'], post_data['id'], post_data["chkIn"], post_data["chkOut"])

    cursor.execute(login_query)

    resp_msg = "success"

    return HttpResponse(resp_msg)


@api_view(['GET', 'POST'])
def reserve_info(request):
    post_data = request.data
    cursor = db.connection.cursor()
    login_query = """
        SELECT A.seq_no
            , A.rm_nm
            , A.rm_addr
            , A.rm_type
            , A.rm_sun_max_pay
            , A.rm_mon_max_pay
            , A.rm_room1_path
            , A.rm_max_pay
            , A.rm_email
            , A.rm_phone
        FROM rooms A 
        where rm_email = '%s'
    """%(post_data['email'])

    cursor.execute(login_query)

    rtn = cursor.fetchall()

    size = len(rtn)

    result = []
    json_data = []

    if size > 0:
        keys = (
        'seq_no', 'rm_nm', 'rm_addr', 'rm_type', 'rm_sun', 'rm_mon', 'rm_room_path', 'rm_max', 'email', 'rm_phone')
        for row in rtn:
            result.append(dict(zip(keys, row)))
            json_data = json.dumps(result)

    else:
        a = {
            "result": "fail"
        }
        json_data = json.dumps(a)

    return HttpResponse(json_data, content_type="application/json")


@api_view(['GET', 'POST'])
def reserve_noti(request):
    post_data = request.data
    cursor = db.connection.cursor()

    login_query = """
        INSERT INTO noti (rm_nm, post_email, get_email, subject, contents) values ('%s', '%s', '%s', '%s', '%s')
    """%(post_data['rm_nm'], post_data['post_email'], post_data['get_email'], post_data['subject'], post_data['content'] )

    cursor.execute(login_query)
    rtn = "success"
    return HttpResponse(rtn)


@api_view(['GET', 'POST'])
def admin_get_noti(request):
    post_data = request.data
    cursor = db.connection.cursor()

    login_query = """
            SELECT seq_no, rm_nm, post_email, get_email, join_date, subject
              FROM noti
             WHERE get_email = '%s'
        """ % (
                post_data['email'])

    cursor.execute(login_query)

    rtn = cursor.fetchall()

    size = len(rtn)

    result = []
    json_data = []

    if size > 0:
        keys = (
            'seq_no', 'rm_nm', 'post_email', 'get_email', 'join_date', 'subject')
        for row in rtn:
            result.append(dict(zip(keys, row)))
            json_data = json.dumps(result, default=str)

    else:
        a = {
            "result": "fail"
        }
        json_data = json.dumps(a)

    return HttpResponse(json_data, content_type="application/json")


@api_view(['GET', 'POST'])
def admin_dtl_noti(request):
    post_data = request.data
    cursor = db.connection.cursor()

    login_query = """
                SELECT seq_no, rm_nm, post_email, get_email, join_date, subject, contents
                  FROM noti
                 WHERE seq_no = '%s'
            """ % (
        post_data['seqNo'])

    cursor.execute(login_query)

    rtn = cursor.fetchall()

    size = len(rtn)

    result = []
    json_data = []

    if size > 0:
        keys = (
            'seq_no', 'rm_nm', 'post_email', 'get_email', 'join_date', 'subject', 'contents')
        for row in rtn:
            result.append(dict(zip(keys, row)))
            json_data = json.dumps(result, default=str)

    else:
        a = {
            "result": "fail"
        }
        json_data = json.dumps(a)

    return HttpResponse(json_data, content_type="application/json")





def file_input(param, seq_no):
    rm_img = Image.open(BytesIO(param.read()))

    image_io = BytesIO()
    rm_img.save(image_io, format=rm_img.format)

    folder = settings.MEDIA_ROOT
    if not os.path.isdir(folder + "/" + str(seq_no)):
        os.mkdir(folder + "/" + str(seq_no))
    # if not os.path.isdir(folder + "/" + str(seq_no) + "/imgRoom"):
    #     os.mkdir(folder + "/" + str(seq_no) + "/imgRoom")

    files = os.listdir(folder + "/" + str(seq_no))

    fs = FileSystemStorage(location=folder + "/" + str(seq_no))
    filename = fs.save("room" + str(len(files)) + "." + str(rm_img.format),
                       ContentFile(image_io.getvalue()))

    return "room" + str(len(files)) + "." + str(rm_img.format)


