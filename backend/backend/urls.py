"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from member.views import register, login, id_check
from htp_test import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path('htp_test/', include('htp_test.urls')),
    path('analyze_img_house/', views.analyze_img_house),
    path('analyze_img_tree/', views.analyze_img_tree),
    path('analyze_img_person/', views.analyze_img_person),
    path('login/', login),
    path('id_check/', id_check),
]

