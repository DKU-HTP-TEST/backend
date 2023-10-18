from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# 아이디, 비밀번호, 이름, email
class Member(AbstractUser):
    user_id = models.CharField(max_length=128, unique=True, verbose_name='아이디')
    password = models.CharField(max_length=225, verbose_name='비밀번호')
    username = models.CharField(max_length=128, verbose_name='이름')
    useremail = models.EmailField(max_length=128, null=True, blank=True, verbose_name="이메일")
    status = models.CharField(max_length=16, default="일반",
        choices = (
            ('일반', '일반'),
            ('탈퇴', '탈퇴'),
            ('휴면', '휴면'),
        )
    )
    REQUIRED_FIELDS = ["user_id"]

    class Meta:
        # db_table = 'htp_member'
        verbose_name = '회원'
        verbose_name_plural = '회원'
