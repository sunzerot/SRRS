import json

from django.http import HttpResponse
from django.shortcuts import render
from django import db
from rest_framework.decorators import api_view

from app.sys.models import Rooms

def index(request):

    obj = Rooms.objects.all().order_by('-seq_no')[0:3]
    return render(request, 'home/main/main.html', {'contents': obj})


@api_view(['GET', 'POST'])
def search(request):

    post_data = request.data

    cursor = db.connection.cursor()
    search = """ 
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
        FROM rooms A left outer join reservation B on A.seq_no = B.rm_no
        where B.seq_no is null
          and A.rm_adult >= '%s'
    
    """ % (post_data['select'])
    cursor.execute(search)
    rtn = cursor.fetchall()

    size = len(rtn)

    result = []
    json_data = []

    if size > 0:
        keys = ('seq_no', 'rm_nm', 'rm_addr', 'rm_type', 'rm_sun', 'rm_mon', 'rm_room_path', 'rm_max', 'email', 'rm_phone')
        for row in rtn:
            result.append(dict(zip(keys, row)))
            json_data = json.dumps(result)

    else:
        a = {
          "result": "fail"
        }
        json_data = json.dumps(a)

    return HttpResponse(json_data, content_type="application/json")

