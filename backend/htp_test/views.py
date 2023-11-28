import random, sys, os, shutil
from datetime import datetime 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import jwt
from member.models import Member
from htp_test.models import HTP, Image_house, Image_tree, Image_person
from htp_test.interprete import res_tree, res_person, res_house

import torch
from torchvision import transforms
# from PIL import Image

from . import views
from yolov5 import detect

import pandas as pd
from PIL import Image


import pandas as pd
from PIL import Image


    



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
            
            image_path = image_model_house.image.path

            #인공지능 실행
            detect.run(source = image_path, weights = r'D:\Capstone_HTP\HTP-backend\backend\htp_test\house_model\best.pt', save_txt=True)
        
            #확장자 제거
            image_file_name, _ = os.path.splitext(os.path.basename(image_model_house.image.name))

            # .txt 확장자를 추가하여 텍스트 파일 경로 생성
            file_path = r'D:\Capstone_HTP\HTP-backend\backend\runs\detect\exp\labels\\'+str(image_file_name)+r'.txt'
            print(image_file_name)
            print(file_path)

            #해석 수행
            house_result = res_house(file_path)

            # 새로운 HTP 객체 생성 및 DB 저장
            htp_obj = HTP(home=house_result, user_id=user, created_date=datetime.now())
            htp_obj.save()

            #결과 나왔으면 이미지 삭제..?
            # image_model = Image.objects.get(pk=)
            # image_model.delete()
            shutil.rmtree(r"D:/CAPSTONE_HTP/HTP-backend/backend/runs/detect/exp/")
            shutil.rmtree(r"D:/CAPSTONE_HTP/HTP-backend/backend/img_house/")
         
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

            image_path = image_model_tree.image.path

            #여기에서 인공지능 분석 등을 수행
            detect.run(weights=r'D:\Capstone_HTP\HTP-backend\backend\htp_test\tree_model\best.pt', source=image_path, project='./result', save_txt=True )
            
            image_file_name, _ = os.path.splitext(os.path.basename(image_model_tree.image.name))

            # .txt 확장자를 추가하여 텍스트 파일 경로 생성
            file_path = r'D:\Capstone_HTP\HTP-backend\backend\result\exp\labels\\'+str(image_file_name)+r'.txt'

            df = pd.read_table(file_path, sep=' ', index_col=0, header=None, names=['label', 'x', 'y', 'w', 'h'])

            # 분석 결과 생성 (랜덤값)

            tree_result = res_tree(df)
            
            # tree_result = random.randint(0, 10)
            
            # 이전에 생성된 HTP 객체 가져오기
            htp_obj = HTP.objects.latest('id')

            # HTP 객체에 결과 값 저장
            htp_obj.tree = tree_result
            htp_obj.save()

            #결과 나왔으면 이미지 삭제..?
            # image_model = Image.objects.get(pk=)
            # image_model.delete()
            shutil.rmtree(r"D:/CAPSTONE_HTP/HTP-backend/backend/result/exp/")
            shutil.rmtree(r"D:/CAPSTONE_HTP/HTP-backend/backend/img_tree/")
         
            # JSON 형식의 응답 생성
            result_data_tree = {
                "image_url": image_model_tree.image.url,
                "tree": tree_result,
            }
        
        return JsonResponse(result_data_tree)

    return JsonResponse({"error": "Invalid request method"})


def analyze_img_person(request):
    if request.method == 'POST':

        # token = request.META.get('HTTP_AUTHORIZATION')
        # decoded = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        # user_id = decoded.get('user_id')

        # user = Member.objects.get(user_id=user_id)

        # 이미지 업로드를 위한 폼에서 'image' 필드 설정
        # POSTMAN에서 KEY 값을 image라 작성해야 함
        uploaded_image = request.FILES.get('image')

        if uploaded_image:
            # Image를 사용하여 이미지 저장
            image_model_person = Image_person(image=uploaded_image)
            image_model_person.save()

            image_path = image_model_person.image.path
            img_w, img_h = Image.open(image_path).size

            #여기에서 인공지능 분석 등을 수행
            detect.run(weights=r'D:\Capstone_HTP\HTP-backend\backend\htp_test\person_model\best.pt', source=image_path, project='./result', save_txt=True )
            
            image_file_name, _ = os.path.splitext(os.path.basename(image_model_person.image.name))

            # # .txt 확장자를 추가하여 텍스트 파일 경로 생성
            file_path = r'D:\Capstone_HTP\HTP-backend\backend\result\exp\labels\\'+str(image_file_name)+r'.txt'

            df = pd.read_table(file_path, sep=' ', index_col=0, header=None, names=['label', 'x', 'y', 'w', 'h'])

            # 분석 결과 생성 (랜덤값)

            person_result = res_person(df, img_w, img_h)
            
            # person_result = random.randint(0, 10)
            
            # 이전에 생성된 HTP 객체 가져오기
            htp_obj = HTP.objects.latest('id')

            # HTP 객체에 결과 값 저장
            htp_obj.person = person_result
            htp_obj.save()

            #결과 나왔으면 이미지 삭제..?
            # image_model = Image.objects.get(pk=)
            # image_model.delete()
            shutil.rmtree(r"D:/CAPSTONE_HTP/HTP-backend/backend/result/exp/")
            shutil.rmtree(r"D:/Capstone_HTP/HTP-backend/backend/img_person/")
         
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
        id = request.GET.get('del_id')

        result = HTP.objects.get(user_id = user, created_date = del_date, id=id)
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


