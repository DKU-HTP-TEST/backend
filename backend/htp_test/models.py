from django.db import models
from member.models import Member

class HTP(models.Model):
    created_date = models.DateField(auto_now=True, verbose_name='생성날짜')
    home = models.TextField(null=True, verbose_name='집결과')
    tree = models.TextField(null=True, verbose_name='나무결과')
    person = models.TextField(null=True, verbose_name='사람결과')
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='사용자아이디', default=1)

class Image_house(models.Model):
    image = models.ImageField(upload_to='img_house/') #upload_to는 파일이 저장되는 디렉토리 경로

class Image_tree(models.Model):
    image = models.ImageField(upload_to='img_tree/')

class Image_person(models.Model):
    image = models.ImageField(upload_to='img_person/')

