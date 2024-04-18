import json
import os
from collections import Counter
from datetime import datetime

def Load_Private_Info(SETTING_PATH) :
    
    # JSON 불러오기
    with open(os.path.join(SETTING_PATH), 'r') as f :
        json_data = json.load(f)
        
        host=json_data['host']
        port = json_data['port']
        user=json_data['user']
        password=json_data['password']
        db=json_data['DB']
        
    return host, port, user, password, db

def json_load(SETTING_PATH) :
    
    # JSON 불러오기
    with open(SETTING_PATH, 'r') as f :
        json_data = json.load(f)
    
    return json_data

def collect_image_list(image_path) :
    
    image_result = []
    image_list = os.listdir(image_path)
    
    for image in image_list :
        
        if image == 'labels' :
            pass
        
        elif image == 'database.csv' :
            pass
        
        else :
            image_result.append(image)
    
    return image_result

def extract_label_result(label_path) :
    
    result = []
    
    data_list = []

    with open(label_path, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            numbers = line.strip().split()  # 공백으로 숫자 분리
            data_list.append(numbers)
            
        first_element = data_list[0]
        
        if len(first_element) == 0 :
            result.append("OK")
        
        else :
            result.append("NG")
            obejct_counting = []
            for line in data_list :
                obejct_counting.append(line[0])
            object_count_result = Counter(obejct_counting)
            result.append(object_count_result)
                
    return result

def convertToDatetime(filetime) :

    # 날짜와 시간 부분으로 분리
    date_part = filetime[:10]  # "2024-04-15"
    time_part = filetime[11:]  # "175221604"

    # 시간 부분을 시:분:초.밀리초 형식으로 변환
    formatted_time = f"{time_part[:2]}:{time_part[2:4]}:{time_part[4:6]}.{time_part[6:]}"

    # 최종 문자열 결합
    formatted_datetime = f"{date_part} {formatted_time}"

    # datetime 객체로 변환하여 정확한 형식 확인
    datetime_obj = datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S.%f")

    # 올바른 형식의 문자열로 출력
    formatted_datetime_string = datetime_obj.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # 밀리초의 마지막 자리를 제거

    return formatted_datetime_string

def convertTofiletime(Datetime) :

    # datetime 객체로 파싱
    datetime_obj = datetime.strptime(Datetime, "%Y-%m-%d %H:%M:%S.%f")

    # 날짜 부분 추출
    date_part = datetime_obj.strftime("%Y-%m-%d")

    # 시간 부분을 연속된 문자열로 변환
    time_part = datetime_obj.strftime("%H%M%S%f")[:9]  # 시간, 분, 초, 밀리초까지 포함

    # 최종 문자열 결합
    original_string = f"{date_part}-{time_part}"

    return original_string
