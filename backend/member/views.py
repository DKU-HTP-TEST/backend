from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .auth import MemberAuth
from .models import Member


# Create your views here.
def register(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        if not Member.objects.filter(user_id=user_id).exists(): # 중복체크
            member = Member (
                user_id = user_id,
                password = request.POST.get("password"),
                username = request.POST.get("username"),
                useremail = request.POST.get("useremail"),
            )
            member.password = make_password(member.password)
            member.save()
            
            return HttpResponse("회원가입 성공")
    return HttpResponse("회원가입 실패")

def login(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")
        user = MemberAuth.authenticate(request, user_id=user_id, password=password)
        print(user_id)
        if user:
            return HttpResponse('login success', status=200)
        else:
            return HttpResponse('login false', status=402)
