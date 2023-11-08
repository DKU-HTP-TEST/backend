from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .auth import MemberAuth
from .models import Member
from .serializer import MyTokenObtainPairSerializer
import jwt


# Create your views here.
def register(request):
    if request.method == 'POST':
        member = Member (
            user_id = request.POST.get("user_id"),
            password = request.POST.get("password"),
            username = request.POST.get("username"),
            useremail = request.POST.get("useremail"),
        )
        member.password = make_password(member.password)
        member.save()
            
    return HttpResponse("회원가입 성공", status=200)


def id_check(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        if not Member.objects.filter(user_id=user_id).exists():
            return HttpResponse("성공", status=200)
        else:
            return HttpResponse("중복", status=400)

def login(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")
        user = MemberAuth.authenticate(request, user_id=user_id, password=password)
        print(user)
        if user:
            token = MyTokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = JsonResponse({
                'access': access_token,
                'refresh': refresh_token,
            }, status=200)

            res.set_cookie('access', access_token)
            res.set_cookie('refresh', refresh_token)
            return res

        else:
            return HttpResponse('login false', status=402)
        
def get_user(request):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded.get('user_id')
        user = Member.objects.get(user_id=user_id)

        res =  {
            'username': user.username,
            'user_id': user.user_id,
            'useremail': user.useremail,
        }
        print(res)
        return JsonResponse(res, status=200)
    
def change_info(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded.get('user_id')
        useremail = request.POST.get("useremail")

def delete(request, user_id):
    if request.method == 'DELETE':
        if user_id:
            try:
                user = Member.objects.get(user_id=user_id)
                if user:
                    user.delete()
                    return HttpResponse({'message': '탈퇴 성공'}, status=200)
            except Member.DoesNotExist:
                return HttpResponse({'message': 'User not found'}, status=404)
        else:
            return HttpResponse({'message': 'user_id is missing in the request'}, status=400)
    else:
        return HttpResponse({'message': 'Invalid request method'}, status=400)

def update_user(request, user_id):
    if request.method == "POST":
        password = request.POST.get("password")
        useremail = request.POST.get("email")
        try:
            user = Member.objects.get(user_id=user_id)
            # user.useremail = useremail
            # return HttpResponse(user.useremail)
            # user = MemberAuth.authenticate(request, user_id=user_id, password=password)
            if password:
                user.password = password
                return HttpResponse(useremail)
            if useremail:
                user.useremail = useremail
                return HttpResponse(useremail)
            user.save()
            # return JsonResponse({'message': 'Update successfully'}, status=200)
            return HttpResponse("수정 성공", status=200)
        except Member.DoesNotExist as e:
            return HttpResponse({'error': f'User with ID {user_id} does not exist'}, status=404)
        except Exception as e:
            return HttpResponse({'error': str(e)}, status=500)
    else:
        return HttpResponse({'error': 'Invalid method'}, status=405)