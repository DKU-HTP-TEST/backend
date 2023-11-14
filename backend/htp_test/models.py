from django.utils import timezone
from django.db import models
from member.models import Member


class HTP(models.Model):
    id = models.AutoField(primary_key=True)
<<<<<<< HEAD
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
=======
    user_id = models.ForeignKey(Member, to_field="user_id", on_delete=models.DO_NOTHING, null=True)
>>>>>>> 7386dd7f4115250a3b24ea024004e4b7c0dd8757
    created_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    home = models.TextField(null=True)
    tree = models.TextField(null=True)
    person = models.TextField(null=True)

class Image_house(models.Model):
    image = models.ImageField(upload_to='img_house/') #upload_to는 파일이 저장되는 디렉토리 경로

class Image_tree(models.Model):
    image = models.ImageField(upload_to='img_tree/')

class Image_person(models.Model):
    image = models.ImageField(upload_to='img_person/')
