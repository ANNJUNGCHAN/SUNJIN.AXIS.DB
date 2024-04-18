import os
os.chdir('/code')
from utils import *
import pymysql

OUTPUT_PATH = "/code/output.json"
DB_SETTING_PATH = "/code/config.json"

# 공장 5개 경로 지정
output = json_load(OUTPUT_PATH)

for factory, db in output.items() :
    
    ### 데이터베이스 연결
    
    print(factory, db)
    dates = os.listdir(db)
    
    # DB SETTING
    host, port, user, password, MySQLdb = Load_Private_Info(DB_SETTING_PATH)

    # connect sql
    conn = pymysql.connect(host= host,
                        port = port,
                        user=user,
                        password=password,
                        db=MySQLdb,
                        charset='utf8')

    cursor = conn.cursor()

    query = f"""
        INSERT INTO {factory} (Factory, machine, datetime, xray, ai, needle, sus, metal, machine_datetime)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    for date in dates :
        
        image_path = os.path.join(db, date)
        image_list = collect_image_list(image_path)
        
        for image in image_list :
            ext_name = image.split('.')[-1]
            label_path = os.path.join(image_path, 'labels', image.replace(ext_name, 'txt'))
            result = extract_label_result(label_path)
            
            info = image.split(".")[0]
            Factory, datetime, machine, xray = info.split("_")[0], info.split("_")[1], info.split("_")[2], info.split("_")[3]
            
            if result[0] == 'OK' :
                ai = result[0]
                needle = 0
                sus = 0
                metal = 0
            
            else :
                ai = result[0]
                needle = result[1]['1']
                sus = result[1]['2']
                metal = result[1]['3']

            convert_datetime = convertToDatetime(datetime)
            key = machine + "_" + datetime
            print(Factory, machine, convert_datetime, xray, ai, needle, sus, metal, key)
            
            cursor.execute(query, (Factory, machine, convert_datetime, xray, ai, int(needle), int(sus), int(metal), key))
            
            conn.commit()