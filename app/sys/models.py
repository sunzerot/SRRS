# -* coding:utf-8 -*-
"""
* @author zerojun
* @version 1.0
* << 개정이력(Modification Information) >>
*   수정일             수정자       수정내용
*   --------------     ----------   -----------------------------------------------------------------------------
*    2019-04-11        zerojun       최초생성
* @since 2019-04-11
"""

from django.db import models


# 예약자
class Member(models.Model):
    seq_no = models.AutoField(primary_key=True)                                     # 시퀀스
    user_name = models.CharField(max_length=20, null=False)                         # 회원 이름
    user_email = models.CharField(max_length=60, null=False)                        # 회원 이메일(아이디)
    user_pwd = models.CharField(max_length=36, null=False)                          # 회원 비밀번호
    user_hp = models.CharField(max_length=20, null=False)                           # 회원 핸드폰 번호
    user_level = models.PositiveSmallIntegerField(null=True, default=1)             # 회원 레벨
    is_use = models.CharField(max_length=1, null=True, default="Y")                 # 사용유무
    join_date = models.DateTimeField(auto_now_add=True)  # 회원가입일
    lastup_time = models.DateTimeField(auto_now=True)  # 마지막 로그인 날짜
    leave_date = models.CharField(max_length=20, null=True, blank=True)             # 회원 탈퇴일
    # user_profile_img_path = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = u'member'

    def __str__(self):
        return u'%s, %s, %s' % (self.user_email, self.user_name, self.user_level)

#
# # 등록자
# class RoomMember(models.Model):
#     seq_no = models.AutoField(primary_key=True)                                     # 시퀀스
#     user_name = models.CharField(max_length=20, null=False)                         # 회원 이름
#     user_email = models.CharField(max_length=60, null=False)                        # 회원 이메일(아이디)
#     user_pwd = models.CharField(max_length=36, null=False)                          # 회원 비밀번호
#     user_hp = models.CharField(max_length=20, null=False)                           # 회원 핸드폰 번호
#     user_level = models.PositiveSmallIntegerField(null=True, default=1)             # 회원 레벨
#     is_use = models.CharField(max_length=1, null=True, default="Y")                 # 사용유무
#     join_date = models.DateTimeField(auto_now_add=True)             # 회원가입일
#     lastup_time = models.DateTimeField(auto_now=True)           # 마지막 로그인 날짜
#     leave_date = models.CharField(max_length=20, null=True, blank=True)             # 회원 탈퇴일
#     user_profile_img_path = models.CharField(max_length=50, null=True)              # 프로필사진경로
#     user_account_num = models.CharField(max_length=100, null=True)                  # 계좌번호
#     user_account_name = models.CharField(max_length=100, null=True)                 # 계좌명
#
#     class Meta:
#         db_table = u'roommember'
#
#     def __str__(self):
#         return u'%s, %s, %s' % (self.user_email, self.user_name, self.user_level)


class Rooms(models.Model):
    seq_no = models.AutoField(primary_key=True)
    rm_nm = models.CharField(max_length=50, null=False)                 # 숙소 이름
    rm_addr = models.CharField(max_length=255, null=False)              # 숙소 주소
    rm_type = models.CharField(max_length=20, null=False)               # 숙소 유형
    rm_child = models.IntegerField(null=True)                           # 어린이
    rm_adult = models.IntegerField(null=True)                           # 어른
    rm_sun_max_pay = models.CharField(max_length=50, null=True)         # 주말금액
    rm_mon_max_pay = models.CharField(max_length=50, null=True)         # 평일금액
    rm_max_day = models.CharField(max_length=50, null=True)             # 최대투숙기간
    rm_chk_in_time = models.CharField(max_length=20, null=False)        # 체크인
    rm_chk_out_time = models.CharField(max_length=20, null=True)        # 체크아웃
    rm_room1_path = models.CharField(max_length=255, null=True)         # 침실1
    rm_room2_path = models.CharField(max_length=255, null=True)         # 침실2
    rm_room3_path = models.CharField(max_length=255, null=True)         # 침실3
    rm_cik_path = models.CharField(max_length=255, null=True)           # 주방
    rm_living_path = models.CharField(max_length=255, null=True)        # 거실
    rm_tol1_path = models.CharField(max_length=255, null=True)          # 화장실1
    rm_tol2_path = models.CharField(max_length=255, null=True)          # 화장실2
    rm_is_use = models.CharField(max_length=1, null=True, default="Y")  # 사용유무
    rm_max_pay = models.CharField(max_length=50, null=True)         # 추가 금액
    rm_email = models.CharField(max_length=60, null=True)
    rm_phone = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = u'rooms'


class Noti(models.Model):
    seq_no = models.AutoField(primary_key=True)
    rm_nm = models.CharField(max_length=50, null=False)
    post_email = models.CharField(max_length=50, null=False)
    get_email = models.CharField(max_length=50, null=False)
    join_date = models.DateTimeField(auto_now_add=True)  # 회원가입일


    class Meta:
        db_table = u'noti'


class Reservation(models.Model):
    seq_no = models.AutoField(primary_key=True)
    rm_no = models.IntegerField(null=False)
    user_id = models.CharField(max_length=255, null=False)
    chk_in_time = models.CharField(max_length=50, null=False)
    chk_out_time = models.CharField(max_length=50, null=False)



    class Meta:
        db_table = u'reservation'
