import pandas as pd

labels_tree = ['나무전체', '기둥', '수관', '가지', '뿌리', '열매', '다람쥐', '나뭇잎', '꽃', '그네']
labels_person = ["사람전체", "머리", "얼굴", "눈", "코", "입", "귀", "머리카락", "목", "상체", "팔", "손", "다리", "발", "단추", "주머니", "운동화", "여자구두"]

def res_tree(df):
    global labels_tree

    res = ""
    index = list(df.index)
    col = list(df.columns)

    tree_size = 0

    for i, label in enumerate(labels_tree):
        num = index.count(i)
        if label == "나무전체":
            if num > 1:
                res += "외로움을 느끼는 경향이 있으며 이중자아를 나타낼 수 있는 특성이 나타납니다."
                
            if df.loc[i, "x"] <= 0.5:
                res += "내향적인 성향을 가지고 있으며 자존감이 낮고 부끄러움을 많이 느끼며 과거에 집착하는 경향이 있습니다. 또한 창의적이고 감수성이 풍부합니다."
            else:
                res += "미래를 중시하며 남성적인 특징을 가지고 있습니다. 또한 동질적 사고와 이질적 사고에 경계가 없으며, 타인에 대한 적대감이나 적대적 태도보다는 지적인 만족을 중시하는 경향이 있습니다."
            
            if df.loc[i, "y"] <= 0.5:
                res += "불안정하고 적절하지 않은 느낌을 자주 경험하며 우울하고 패배감을 갖는 경향이 있습니다."
            
            tree_size = df.loc[i, "w"] * df.loc[i, "h"]

        elif label == "기둥":
            if num == 0:
                res += "자아강도가 극도로 악되었거나 와해되어 정신증적 상태에 있다. 때로는 지나치게 부적절하다고 느끼며 자기를 억제하거나 피하는 경향이 강할 수 있습니다."

        elif label == "수관":
            if df.loc[i, "w"] * df.loc[i, "h"] <= tree_size // 2:
                res += "정서적으로 빈곤함을 느끼고 있는 모습이 보일 수 있습니다."
            else:
                res += "공상적인 면을 가지고 있지만 현실적인 전망이 부족하며, 환경에 대해 적극적으로 대응하고 때로는 공격적인 태도를 보일 수 있습니다."

        elif label == "가지":
            if num == 0:
                res += "세상과의 상호작용에 있어서 매우 억제되어 있는 것으로 보입니다."
            elif num > 5:
                res += "많은 일을 하고 싶어하며 대인 관계가 활발하지만 과도한 의욕을 보이는 경향이 있습니다."
            else:
                res += "세상과의 상호작용에 억제적인 경향이 있으며, 때때로 우울하거나 우울감을 느끼는 것으로 보입니다."

        elif label == "뿌리":
            continue

        elif label == "열매":
            res += "애정의 결핍의 모습이 나타나며 사랑과 관심에 대한 강한 욕구가 있는 것으로 보입니다."

        elif label == "그네":
            res += "우울함을 많이 느끼고 자주 외로움을 경험하는 경향이 있습니다."

    return res

def res_person(df, img_w, img_h):
    global labels_person

    res = ""
    index = list(df.index)
    col = list(df.columns)

    person_size = 0

    # 클래스에 따른 해석 추가
    for i, label in enumerate(labels_person):
        num = df[df.index == i].shape[0]        # 데이터프레임에서 해당 레이블의 행 수를 가져옴
        person_size = 0
        face_size = 0

        if label =="사람전체":
            # i를 사용하지 않고 해당 레이블에 해당하는 행의 인덱스를 가져옴
            matching_rows = df[df.index == i]
            if not matching_rows.empty:
                index_person = df[df.index == i].index[0]
                person_size = df.loc[index_person, 'w'] * df.loc[index_person, 'h']
                size = person_size / (img_w * img_h)            # 전체 그림 크기와 객체 크기 비
                
                if size <= 0.35:
                    res += "대인관계에서 무력감과 열등감을 느끼며 불안과 우울한 경향이 있습니다."
                elif size >= 0.65:
                    res += "충동적이며 공격적인 모습이 나타납니다."
                else:
                    res += ""   # 정상적인 내용 추가

                if df[df.index == i]['x'].values[0] <= 0.5:
                    res += "내향적이며 소극적인(강박적이거나 우울한) 성향을 보이고 있습니다."
                else:
                    res += "외향적이고 이기적이며 공격적인 성향을 가지고 있으며, 불안감과 분노를 느낄 수 있습니다."
                
                if df[df.index == i]['y'].values[0] <= 0.5:
                    res += "강한 심리적 억압을 느끼고 있으며, 우울, 두려움, 불안, 그리고 열등감을 경험할 수 있습니다."
            else:
                # 적절한 처리를 수행하거나 오류를 처리하는 등의 작업을 추가할 수 있습니다.
                print(f"No matching rows found for index {i}")

        elif label == "머리":
            if num > 0:
                size = df[df.index == i]['w'].values[0] * df[df.index == i]['h'].values[0] / person_size    # 전체 사람 크기와 머리 크기 비
                if size <= 0.3:
                    res += "자신의 지적능력, 공상세계와 관련된 부적절감을 느끼고 있으며 지적인 표현과 관련하여 수동적이고 억제적이고 위축된 태도를 보입니다."
                elif size >= 0.6:
                    res += "지적능력에 대해 불안감을 느끼지만 이를 과도하게 보상하고자 하는 욕구가 나타나는 것으로 보입니다."
            if num == 0:
                res += "사고나 신경학적인 측면에서의 장애 가능성을 고려할 수 있습니다."

        elif label == "얼굴":
            if num > 0:
                face_size = df[df.index == i]['w'].values[0] * df[df.index == i]['h'].values[0]
                res += ''

        elif label == "눈":
            if num > 0:
                size = df[df.index == i]['w'].values[0] * df[df.index == i]['h'].values[0] / face_size  # 얼굴 크기와 눈 크기 비
                if size >= 0.4:
                    res += "타인과의 정서적 교류에 있어 지나치게 예민할 수 있습니다."
                elif size <= 0.1:
                    res += "사회적 상호작용에서 위축되고 회피하려는 경향이 있으며, 내성적이고 자아도취에 빠지며, 관계회피도 보일 수 있습니다."

        elif label == "코":
            if num == 0:
                res += "타인에게 어떻게 보일지에 매우 예민하고 두려워하며, 사회적 상황에서 위축되고 회피적입니다."
            if num > 0:
                size = df[df.index == i]['w'].values[0] * df[df.index == i]['h'].values[0] / face_size
                if size >= 0.4:
                    res += "주변 사람들과의 관계에서 정서적 자극에 예민하며 외모에 지나친 관심을 갖는 경향이 있으며, 공격적이고 강박적이며 분노를 폭발시키기도 합니다."
                elif size <= 0.1:
                    res += "타인과의 감정 교류에 대해 수동적이고 회피적인 모습이 나타납니다."
                
        elif label == "입":
            if num == 0:
                res += "타인과의 애정의 교류에 있어서 좌절감이나 무능력감, 위축감, 양가감정을 느끼는 것으로 보입니다."
            if num > 0:
                size = df[df.index == i]['w'].values[0] * df[df.index == i]['h'].values[0] / face_size
                if size >= 0.4:
                    res += "타인과의 정서적 교류, 애정의 교류에 있어서 불안감을 느끼지만 과도하게 적극적이고 주장적이고 심지어 공격적인 태도를 취함으로써 역공포적으로 이러한 불안감을 보상하고자 하는 모습이 나타날 수 있습니다."
                elif size >= 0.1:
                    res += "내적인 상처를 받지 않으려고 정서적 상호작용을 회피하고자 합니다."

        elif label == "귀":            
            if num == 0:
                res += "자신의 감정을 표현하는데 대해 불안하고 자신이 없으며 사회적 상황이나 감정 교류 상황을 회피하고 위축되는 경향이 나타납니다."
            if num > 0:
                size = df[df.index == i]['w'].values[0] * df[df.index == i]['h'].values[0] / face_size
                if size >= 0.4:
                    res += "대인관계 상황에서 너무 예민함을 의미합니다."
                elif size <= 0.1:
                    res += "정서적 자극을 피하고 싶고 위축되어 보입니다."

        elif label == "머리카락":
            res += ''
            
        elif label == "목":
            res += ''
            
        elif label == "상체":
            res += ''
            
        elif label == "팔":
            res += ''
            
        elif label == "손":
            res += ''
            
        elif label == "다리":
            res += ''
            
        elif label == "발":
            res += ''
            
        elif label == "단추":
            res += ''
            
        elif label == "주머니":
            res += ''
            
        elif label == "운동화":
            res += ''
            
        elif label == "여자구두":
            res += ''


    return res

def res_house(file_path):
    
    class_counts = [0] * 15

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return ['File not found.']
    
    analysis = []
    # img_width = 1280

    for line in lines:
        parts = line.split()
        label = int(parts[0])

        # 클래스 개수 계산
        class_counts[label] += 1
        
        if label == 0:
            x, y, w, h = map(float, parts[1:])
            cx = x #+ w/2*img_width
            cy = y #+ h/2*img_width
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
        
    if cx < 0.4:  #집 전체가 좌측 
        analysis.append('내향적 열등감을 지니고 있습니다. ')
    if cx > 0.6:  #집 전체가 우측
        analysis.append('외향성 활동성을 지니고 있습니다. ')
    if cy < 0.3:  # 집 전체가 하단
        analysis.append('안정감을 가지지만 우울하고 위축되어 있으며 패배감이 짙습니다. ')
    if rw-ww > 0.08: #지붕이 지나치게 큰 경우
        analysis.append('대인관계에서는 좌절감을 느끼고 위축되어 내면의 공상 속에서 즐거움과 욕구 충족을 추구합니다.')
    if rw - ww < 0: #지붕이 작은 경우
        analysis.append('내적으로 생각과 감정에 대한 탐구가 부족하며, 회피 경향, 억압, 그리고 정서적 빈약이 나타날 수 있습니다. ')
    if door*20 < house:  #문이 큰 경우
        analysis.append('수줍음, 까다로움, 사회성 결핍, 현실에서 도피하는 성향이 드러날 수 있습니다. 이는 대인 관계나 사회적 활동에 대한 도전을 피하려는 경향을 나타냅니다. ')
    elif door*4 > house:  #문이 작은 경우
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

    return "".join(analysis)