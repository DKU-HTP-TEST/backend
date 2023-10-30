from django.contrib import admin
from .models import HTP
from .models import Image_house, Image_tree, Image_person

admin.site.register(HTP)
admin.site.register(Image_house)
admin.site.register(Image_tree)
admin.site.register(Image_person)
# Register your models here.