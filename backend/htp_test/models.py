from django.db import models

class HTP(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateField(auto_now=True)
    home = models.TextField()
    tree = models.TextField()
    person = models.TextField()