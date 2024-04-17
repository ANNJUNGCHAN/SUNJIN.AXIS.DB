import os
os.chdir("/code")
import pymysql
import time

from utils import * 

while True :

    try :
        
        LOG_PATH = "/Drive/SSD1/AICCTV_LOG"
        VIDEO_PATH = "/Drive/HDD/AICCTV_VIDEO"

        log_list = os.listdir(LOG_PATH)
        log_list = filter_log(log_list)
        
        # connect sql
        conn = pymysql.connect(host='193.202.10.89',
                            port = 10000,
                            user='root',
                            password='sunjin1234',
                            db='AICCTV_DB',
                            charset='utf8')

        cursor = conn.cursor()

        query = """
            INSERT INTO AICCTVDB (Farm, House, Counter, start_time, end_time, incount, outcount)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        if len(log_list) == 0 :
            
            time.sleep(60*60) # 한시간
            pass
        
        else :
            
            for path in log_list :
                
                Farm, House, COUNTER, start_time, end_time, in_count, out_count = extract_todb(LOG_PATH, path)
                
                # 만약, 둘다 0이면 비디오와 로그 모두 제거
                if (in_count == '0') and (out_count == '0') :
                    os.remove(os.path.join(VIDEO_PATH, path.replace('.txt','.avi')))
                    os.remove(os.path.join(LOG_PATH, path))
                
                # 만약, 둘 중 하나가 0이 아니면, 로그는 기록으로 올린 후, 로그만 제거
                else :
                    
                    print(Farm, House, COUNTER, start_time, end_time, in_count, out_count)
                        
                    cursor.execute(query, (Farm, House, COUNTER, start_time, end_time, int(in_count), int(out_count)))

                    # end
                    conn.commit()
                    
                    os.remove(os.path.join(LOG_PATH, path))
    
    except Exception as e :
        print(e)