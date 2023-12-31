from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('id_check/', views.id_check),
    path('get_user/', views.get_user),
    path('delete/<str:user_id>/', views.delete),
    path('update_user/', views.update_user),
]