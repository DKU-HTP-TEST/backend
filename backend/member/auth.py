from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import check_password
from .models import Member

class MemberAuth:
    def authenticate(request, user_id=None, password=None, *args, **kwargs):
        if not user_id or not password:
            if request.user.is_authernticated:
                return request.user
            return None

        try:
            member= Member.objects.get(user_id=user_id)
        except Member.DoesNotExist:
            return None
        if check_password(password,member.password):
            if member.status=="일반":
                return member # 로그인 성공 

        return None