import random
from datetime import datetime 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import HTP, Image_house, Image_tree, Image_person
from . import views


# Create your views here.

def analyze_img_house(request):
    if request.method == 'POST':

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
            htp_obj = HTP.objects.create(home=house_result, created_date=datetime.now())
            htp_obj.save()
            #결과 나왔으면 이미지 삭제..?
            # image_model = Image.objects.get(pk=)
            # image_model.delete()
         
            # JSON 형식의 응답 생성
            result_data = {
                "image_url": image_model_house.image.url,
                "house": house_result,
            }
        
        return JsonResponse(result_data)

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
            result_data = {
                "image_url": image_model_tree.image.url,
                "tree": tree_result,
            }
        
        return JsonResponse(result_data)

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
            result_data = {
                "image_url": image_model_person.image.url,
                "tree": person_result,
            }
        
        return JsonResponse(result_data)

    return JsonResponse({"error": "Invalid request method"})

def result(request, user_id):
    try:
        result = HTP.objects.get(pk=user_id)    #...?어떤거랑 외래키?
        result_data = {
            "home": result.home,
            "tree": result.tree,
            "person": result.person,
            "created_date": result.created_date,
        }
        return JsonResponse(result_data)
    except HTP.DoesNotExist:
        return JsonResponse({"error": "Result not found"}, status=404)

def del_result(request):
    if request.method == 'DELETE':
        user_id = request.data.get('user_id')
        del_date = request.data.get('del_date')

        result = HTP.objects.get(user_id = user_id, create_date = del_date)
        result.delete()
        return HttpResponse("삭제 성공", status=200)
    else:
        return HttpResponse('error', status = 400)

