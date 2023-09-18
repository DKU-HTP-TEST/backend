from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import make_password
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
