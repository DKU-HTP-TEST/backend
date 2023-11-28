import random, sys, os, shutil
from datetime import datetime 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import jwt
from member.models import Member
from htp_test.models import HTP, Image_house, Image_tree, Image_person
from htp_test.interprete import res_tree, res_person

import torch
from torchvision import transforms
# from PIL import Image

from . import views
from yolov5 import detect

import pandas as pd
from PIL import Image


import pandas as pd
from PIL import Image


# from collections import defaultdict
# # 각 클래스의 개수를 저장할 딕셔너리
# class_counts = defaultdict(int)



    #크기 계싼이 필요한 클래스: 지붕, 문, 집 전체, 나무(?)
    #개수가 필요한 클래스: 창문 -> 해결
    #유무가 필요한 클래스: 지붕, 창문, 문, 연기, 울타리, 길, 연못, 산, 꽃, 잔디, 테양 -> 해결
    # 클래스에 따른 해석 추가
    



# Create your views here.
def res_house(file_path):
    
    class_counts = [0] * 15

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return ['File not found.']
    
    analysis = []
    img_width = 1280

    for line in lines:
        parts = line.split()
        label = int(parts[0])

        # 클래스 개수 계산
        class_counts[label] += 1
        
        if label == 0:
            x, y, w, h = map(float, parts[1:])
            cx = x + w/2*img_width
            cy = y + h/2*img_width
            house = w*h
        if label == 1:
            x, y, w, h = map(float, parts[1:])
            rw = w
        
        if label == 2:
            x, y, w, h = map(float, parts[1:])
            ww = w
    
        if label == 3:
            x, y, w, h = map(float, parts[1:])
            door = w*h
        
    if cx < 360:  #집 전체가 좌측 
        analysis.append('내향적 열등감을 지니고 있습니다. ')
    if cx > 920:  #집 전체가 우측
        analysis.append('외향성 활동성을 지니고 있습니다. ')
    if cy < 300:  # 집 전체가 하단
        analysis.append('안정감을 가지지만 우울하고 위축되어 있으며 패배감이 짙습니다. ')
    if rw-ww > 0.08: #지붕이 지나치게 큰 경우
        analysis.append('대인관계에서는 좌절감을 느끼고 위축되어 내면의 공상 속에서 즐거움과 욕구 충족을 추구합니다.')
    if rw - ww < 0.02: #지붕이 작은 경우
        analysis.append('내적으로 생각과 감정에 대한 탐구가 부족하며, 회피 경향, 억압, 그리고 정서적 빈약이 나타날 수 있습니다. ')
    if door*20 < house: 
        analysis.append('수줍음, 까다로움, 사회성 결핍, 현실에서 도피하는 성향이 드러날 수 있습니다. 이는 대인 관계나 사회적 활동에 대한 도전을 피하려는 경향을 나타냅니다. ')
    elif door*4 > house:
        analysis.append('사회적 접근 가능성이 과다할 수 있고, 사회적인 인정이나 수용에 지나치게 의존적이라 판단할 수 있습니다. ')

    # 각 클래스에 대한 해석(유무 판단)
    if class_counts[1] == 0:  #지붕이 없는 경우
        analysis.append('공상활동, 내적인 인지과정을 표현하지 못하고 있을 수 있습니다.')
    if class_counts[3] == 0:   #문이 없는 경우
        analysis.append('관계에 대한 회피, 고립, 그리고 정서적인 위축이 나타납니. 대인 관계를 피하거나 소통에 어려움을 겪을 수 있으며, 감정적인 연결이 상대적으로 빈약할 수 있다는 것을 나타냅니다.')
    if class_counts[4] == 0:   #창문이 없는 경우
        analysis.append('폐쇄적 사고 양상이 도드라지며 환경에 대한 관심의 결여와 적의가 드러날 수 있습니다. 주변 환경과의 상호작용에서 어려움을 겪을 수 있거나, 대인 관계에서 감정적인 거리를 둘 수 있는 특징을 나타냅니다.')
    if class_counts[4] > 2:  #창문이 3개 이상인 경우
        analysis.append('과도한 자기 개방과 강한 타인과의 관계 형성 욕구가 나타납니다. 불안의 보상심리와 개방적인 환경과의 갈망이 나타납니다. ')
    if class_counts[6] > 0:
        analysis.append('마음속의 긴장을 가지고 있으며 가정 내 불화나 갈등에 대한 정서적 긴장감을 반영할 수 있음 짐작할 수 있습니다. ')
    if class_counts[7] > 0:  #울타리
        analysis.append('자신을 지키고자 하며, 방어적이고 열등감을 느낄 수도 있습니다. 안정감을 중요시하며, 타인으로부터의 간섭이나 방해를 원치 않는 심리적 특징을 나타납니다. ')
    if class_counts[8] > 0:  # 길
        analysis.append('사회적 상호관계 환영하는 특징이 나타납니다. ')
    if class_counts[9] > 0:  # 연못
        analysis.append('가정에 대한 우울한 정서감정이 나타납니다. ')
    if class_counts[10] > 0: #산
        analysis.append('도피와 안정을 추구하고, 방어적 태도와 함께 독립의 욕구가 있을 수 있습니다. ')
    if class_counts[14] > 0:  # 태양
        analysis.append('당신이 아동일 경우 일반적이나, 성인일 경우 강력한 부모와 같은 자기대상존재를 갈망하고 있음을 암시할 수 있습니다. ')

    print("Class Counts:", class_counts)
    print("Analysis:", analysis)

    
    return "".join(analysis)



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
            detect.run(source = image_path, weights = 'C:/Users/윤해빈/OneDrive/바탕 화면/캡스톤 2학기/Backend/backend/htp_test/house_model/best.pt', save_txt=True)
        
            #확장자 제거
            image_file_name, _ = os.path.splitext(os.path.basename(image_model_house.image.name))

            # .txt 확장자를 추가하여 텍스트 파일 경로 생성
            file_path = f'C:/Users/윤해빈/OneDrive/바탕 화면/캡스톤 2학기/Backend/backend/runs/detect/exp/labels/'+str(image_file_name)+r'.txt'
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
            shutil.rmtree(r"C:/Users/jimin/OneDrive/바탕 화면/2학기-onedrive/@학교 수업/캡스톤디자인2/HTP_backend/backend/runs/detect/exp/")
         
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
            detect.run(weights=r'C:/Users/jimin/OneDrive/바탕 화면/2학기-onedrive/@학교 수업/캡스톤디자인2/HTP_backend/backend/htp_test/tree_model/best.pt', source=image_path, project='./result', save_txt=True )
            
            image_file_name, _ = os.path.splitext(os.path.basename(image_model_tree.image.name))

            # .txt 확장자를 추가하여 텍스트 파일 경로 생성
            file_path = r'C:/Users/jimin/OneDrive/바탕 화면/2학기-onedrive/@학교 수업/캡스톤디자인2/HTP_backend/backend/result/exp/labels/'+str(image_file_name)+r'.txt'

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
            shutil.rmtree(r"C:/Users/jimin/OneDrive/바탕 화면/2학기-onedrive/@학교 수업/캡스톤디자인2/HTP_backend/backend/result/exp/")
         
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
            detect.run(weights=r'C:/Users/jimin/OneDrive/바탕 화면/2학기-onedrive/@학교 수업/캡스톤디자인2/HTP_backend/backend/htp_test/tree_model/best.pt', source=image_path, project='./result', save_txt=True )
            
            image_file_name, _ = os.path.splitext(os.path.basename(image_model_person.image.name))

            # # .txt 확장자를 추가하여 텍스트 파일 경로 생성
            file_path = r'C:/Users/jimin/OneDrive/바탕 화면/2학기-onedrive/@학교 수업/캡스톤디자인2/HTP_backend/backend/result/exp/labels/'+str(image_file_name)+r'.txt'

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
            shutil.rmtree(r"C:/Users/jimin/OneDrive/바탕 화면/2학기-onedrive/@학교 수업/캡스톤디자인2/HTP_backend/backend/result/exp/")
         
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


