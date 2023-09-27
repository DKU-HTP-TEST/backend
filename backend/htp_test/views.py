import random
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import HTP, Image
from . import views


# Create your views here.

def analyze_img(request):
    if request.method == 'POST':

        # 이미지 업로드를 위한 폼에서 'image' 필드 설정
        # POSTMAN에서 KEY 값을 image라 작성해야 함
        uploaded_image = request.FILES.get('image')

        if uploaded_image:
            # Image를 사용하여 이미지 저장
            image_model = Image(image=uploaded_image)
            image_model.save()

            #여기에서 인공지능 분석 등을 수행


            # 분석 결과 생성 (랜덤값)
            home_result = random.randint(0, 10)
            tree_result = random.randint(0, 10)
            person_result = random.randint(0, 10)
            
            # 새로운 HTP 객체 생성 및 데이터베이스에 저장
            result = HTP.objects.create(home=home_result, tree=tree_result, person=person_result)

            #결과 나왔으면 이미지 삭제..?
            # image_model = Image.objects.get(pk=)
            # image_model.delete()
        
         
            # JSON 형식의 응답 생성
            result_data = {
                "image_url": image_model.image.url,
                "home": home_result,
                "tree": tree_result,
                "person": person_result,
            }
        
        return JsonResponse(result_data)

    return JsonResponse({"error": "Invalid request method"})



def result(request, result_id):
    try:
        result = HTP.objects.get(pk=result_id)    #...?어떤거랑 외래키?
        result_data = {
            "home": result.home,
            "tree": result.tree,
            "person": result.person,
            "created_date": result.created_date,
        }
        return JsonResponse(result_data)
    except HTP.DoesNotExist:
        return JsonResponse({"error": "Result not found"}, status=404)


