from django.db import models
from member.models import Member


class HTP(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now=True)
    home = models.TextField()
    tree = models.TextField()
    person = models.TextField()

class Image_house(models.Model):
    image = models.ImageField(upload_to='img_house/') #upload_to는 파일이 저장되는 디렉토리 경로

class Image_tree(models.Model):
    image = models.ImageField(upload_to='img_tree/')

class Image_person(models.Model):
    image = models.ImageField(upload_to='img_person/')

