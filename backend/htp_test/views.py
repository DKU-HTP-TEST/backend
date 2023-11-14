import random
from datetime import datetime 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import jwt
from member.models import Member
from .models import HTP, Image_house, Image_tree, Image_person
from member.models import Member

from . import views


# Create your views here.

def analyze_img_house(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        user_id = decoded.get('user_id')

        user = Member.objects.get(user_id=user_id)
        print(user)

        # 이미지 업로드를 위한 폼에서 'image' 필드 설정
        # POSTMAN에서 KEY 값을 image라 작성해야 함
        uploaded_image = request.FILES.get('image')

        if uploaded_image:
            # Image를 사용하여 이미지 저장
            image_model_house = Image_house(image=uploaded_image)
            image_model_house.save()

            #여기에서 인공지능 분석 등을 수행


            # 분석 결과 생성 (랜덤값)
            house_result = random.randint(0, 10)
            
            # 새로운 HTP 객체 생성 및 DB 저장
            htp_obj = HTP(home=house_result, user_id=user, created_date=datetime.now())
            htp_obj.save()
            #결과 나왔으면 이미지 삭제..?
            # image_model = Image.objects.get(pk=)
            # image_model.delete()
         
            # JSON 형식의 응답 생성
            result_data_house = {
                "image_url": image_model_house.image.url,
                "house": house_result,
            }
        
        return JsonResponse(result_data_house)

    return JsonResponse({"error": "Invalid request method"})

def analyze_img_tree(request):
    if request.method == 'POST':

        # 이미지 업로드를 위한 폼에서 'image' 필드 설정
        # POSTMAN에서 KEY 값을 image라 작성해야 함
        uploaded_image = request.FILES.get('image')

        if uploaded_image:
            # Image를 사용하여 이미지 저장
            image_model_tree = Image_tree(image=uploaded_image)
            image_model_tree.save()

            #여기에서 인공지능 분석 등을 수행


            # 분석 결과 생성 (랜덤값)
            tree_result = random.randint(0, 10)
            
            # 이전에 생성된 HTP 객체 가져오기
            htp_obj = HTP.objects.latest('id')

            # HTP 객체에 결과 값 저장
            htp_obj.tree = tree_result
            htp_obj.save()

            #결과 나왔으면 이미지 삭제..?
            # image_model = Image.objects.get(pk=)
            # image_model.delete()
         
            # JSON 형식의 응답 생성
            result_data_tree = {
                "image_url": image_model_tree.image.url,
                "tree": tree_result,
            }
        
        return JsonResponse(result_data_tree)

    return JsonResponse({"error": "Invalid request method"})

def analyze_img_person(request):
    if request.method == 'POST':

        # 이미지 업로드를 위한 폼에서 'image' 필드 설정
        # POSTMAN에서 KEY 값을 image라 작성해야 함
        uploaded_image = request.FILES.get('image')

        if uploaded_image:
            # Image를 사용하여 이미지 저장
            image_model_person = Image_person(image=uploaded_image)
            image_model_person.save()

            #여기에서 인공지능 분석 등을 수행


            # 분석 결과 생성 (랜덤값)
            person_result = random.randint(0, 10)
            
            # 이전에 생성된 HTP 객체 가져오기
            htp_obj = HTP.objects.latest('id')

            # HTP 객체에 결과 값 저장
            htp_obj.person = person_result
            htp_obj.save()

            #결과 나왔으면 이미지 삭제..?
            # image_model = Image.objects.get(pk=)
            # image_model.delete()
        
            # JSON 형식의 응답 생성
            result_data_person = {
                "image_url": image_model_person.image.url,
                "person": person_result,
            }
        
        return JsonResponse(result_data_person)

    return JsonResponse({"error": "Invalid request method"})

def get_dates(request):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded.get('user_id')
        user = Member.objects.get(user_id=user_id)

        object = HTP.objects.filter(user_id=user)
        dates = [obj.created_date for obj in object]
        id = [obj.id for obj in object]
        print(dates)
        result_data = {
            "dates": dates,
            "id": id,
        }
        return JsonResponse(result_data, status=200)


def result(request):
    if request.method == 'GET':
        
        token = request.META.get('HTTP_AUTHORIZATION')
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded.get('user_id')

        user = Member.objects.get(user_id=user_id)
        date = request.GET.get('date')
        id = request.GET.get('id')
        
        result = HTP.objects.get(user_id=user, created_date=date, id=id)
        result_data = {
            "home": result.home,
            "tree": result.tree,
            "person": result.person,
        }
        
        return JsonResponse(result_data)

def del_result(request):
    if request.method == 'DELETE':

        token = request.META.get('HTTP_AUTHORIZATION')
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded.get('user_id')

        user = Member.objects.get(user_id=user_id)

        del_date = request.GET.get('del_date')

        result = HTP.objects.get(user_id = user, created_date = del_date)
        result.delete()

        return HttpResponse("삭제 성공", status=200)
    
    else:
        return HttpResponse('error', status = 400)
    
def test_result(request):
    if request.method == "GET":
        test_res = HTP.objects.latest('id')
        test_res_data = {
            "home": test_res.home,
            "tree": test_res.tree,
            "person": test_res.person,
        }
        return JsonResponse(test_res_data)


