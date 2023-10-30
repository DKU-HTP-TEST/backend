from django.urls import path
from . import views

urlpatterns = [
    path('analyze_img_house/', views.analyze_img_house),
    path('analyze_img_tree/', views.analyze_img_tree),
    path('analyze_img_person/', views.analyze_img_person)
]