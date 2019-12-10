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


# 등록자
class RoomMember(models.Model):
    seq_no = models.AutoField(primary_key=True)                                     # 시퀀스
    user_name = models.CharField(max_length=20, null=False)                         # 회원 이름
    user_email = models.CharField(max_length=60, null=False)                        # 회원 이메일(아이디)
    user_pwd = models.CharField(max_length=36, null=False)                          # 회원 비밀번호
    user_hp = models.CharField(max_length=20, null=False)                           # 회원 핸드폰 번호
    user_level = models.PositiveSmallIntegerField(null=True, default=1)             # 회원 레벨
    is_use = models.CharField(max_length=1, null=True, default="Y")                 # 사용유무
    join_date = models.DateTimeField(auto_now_add=True)             # 회원가입일
    lastup_time = models.DateTimeField(auto_now=True)           # 마지막 로그인 날짜
    leave_date = models.CharField(max_length=20, null=True, blank=True)             # 회원 탈퇴일
    user_profile_img_path = models.CharField(max_length=50, null=True)              # 프로필사진경로
    user_account_num = models.CharField(max_length=100, null=True)                  # 계좌번호
    user_account_name = models.CharField(max_length=100, null=True)                 # 계좌명

    class Meta:
        db_table = u'roommember'

    def __str__(self):
        return u'%s, %s, %s' % (self.user_email, self.user_name, self.user_level)
