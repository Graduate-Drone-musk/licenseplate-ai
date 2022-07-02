import os
import glob
import cv2
import time
import boto3
import secret


def s3_res_connect():
    try:
        s3 = boto3.resource(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id=secret.AWS_KEY["access_id"],
            aws_secret_access_key=secret.AWS_KEY["access_key"]
        )
    except Exception as e:
        print(e)
        print("123")
    else:
        for bucket in s3.buckets.all():
            bucket_name = bucket.name
        return s3, bucket_name    

def get_today():
    now = time.localtime(time.time()) 
    now_year = str(now.tm_year)
    now_month = '0'+str(now.tm_mon) if now.tm_mon//10==0 else str(now.tm_mon) 
    now_day =  '0'+str(now.tm_mday) if now.tm_mday//10==0 else str(now.tm_mday)
    return now_year + now_month + now_day    

def compare_file(result_dir):
    today_name = get_today()
    
    upload_path = os.path.join(result_dir, today_name)   # 오늘 날짜로 변경해야됨
    time_locate = os.listdir(upload_path)                # 205207465_01234_56789
    
    time_list = []      # 시 분 초
    locate_list = []    # 위, 경도

    for path in time_locate:
        time, locate = path.split("_")
        time_list.append(time)
        locate_list.append(locate)                    

    length = len(locate_list)
    for i in range(length-1):
        for j in range(i+1, length):   
            if (locate_list[i] == locate_list[j]) \
                and (abs(int(time_list[i]) - int(time_list[j])) <= 10000):
                
                check_illegal(f"{time_list[i]}_{locate_list[i]}", f"{time_list[j]}_{locate_list[j]}", upload_path)

def check_illegal(pre_time, last_time, upload_path=""):
    today_name = get_today()
    os.makedirs('./illegal_file/{}'.format(today_name), exist_ok = True)
    illegal_path = './illegal_file/{}'.format(upload_path.split("\\")[-1])
    
    car_txt = []       # 딥러닝 result.txt 번호판 목록
    illegal_list = []  # 불법 주차 번호판 목록
    ille_info = []     # 번호판의 사진 경로 정보
    time_list = [pre_time, last_time]
 
    # path/시간_위도경도
    path_list = [os.path.join(upload_path, path) for path in time_list]
    for i, crop in enumerate(path_list):
        car_txt.append([])
        crop_path = os.path.join(crop, 'crop')
        txt_path = glob.glob(os.path.join(crop_path, '*.txt'))
        with open(*txt_path, 'r', encoding = 'utf-8') as f:    # txt 파일 읽기
            car_name = f.readlines()
            for compare_txt in car_name:
                car_txt[i].append((compare_txt.split(' ')[1].split('\n')[0]))  # ocr 결과만 
   
    for i in range(len(car_txt[0])):           # 20시 (4)
        for j in range(len(car_txt[1])):       # 21시 (10)
            if car_txt[0][i] == car_txt[1][j]:       # 1시간 내에 같은 차량이 있다면
                illegal_list.append(car_txt[0][i])   # 검거
 
    for illegal_car in illegal_list:                 # 검거된 번호판 중 전체 차량 정보를 탐색
        for car_info in car_name:  
            if illegal_car in car_info:              # 차량 정보에 포함되면
                ille_info.append(car_info)           # 불법 차량 정보 넣기

    
    for i in ille_info: 
        crop_img_path = i.split("\\")[-1].split(" ")[0]                       # crop 이미지 경로 불러오기
        crop_img = cv2.imread(os.path.join(crop_path, crop_img_path), cv2.IMREAD_COLOR)
        cv2.imwrite(illegal_path + '\\' + crop_img_path, crop_img)            # 불법 주차 crop 이미지 넣기

        origin_path = crop_img_path.split("_")[:2]                            # 불법 주차 원본 이미지 경로 불러오기
        origin_path = '_'.join(origin_path) + '.jpg'

        origin_img = cv2.imread(os.path.join(path_list[1], origin_path), cv2.IMREAD_COLOR)
        cv2.imwrite(illegal_path + '\\' + origin_path, origin_img)            # 불법 주차 원본 이미지 넣기

    for make_txt in illegal_list:
        with open(illegal_path + '\\illegal.txt' , 'a') as f:                 # 불법 주차 txt 파일 쓰기
            f.write(make_txt + '\n')

    upload_illegal_image(illegal_path)

def upload_illegal_image(illegal_path):
    ille_list = os.listdir(illegal_path)       # illegal 파일 목록 불러오기
    upload_illegal(ille_list, illegal_path)

         
def upload_illegal(ille_list, illegal_path):   # illegal 파일 업로드 
    s3, bucket_name = s3_res_connect()
    today_name = get_today()
    root_dir = "illegal_file/"
    for list in ille_list:
        temp = list.split('_')
        if len(temp) == 3:
            temp[2] = '_' + temp[2]            # 작대기 2개 추가
        temp = '_'.join(temp)    
        s3.Bucket(bucket_name).upload_file(illegal_path + '/' + list, root_dir + '{}'.format(today_name) + '/' + temp)        # s3에 업로드
              
def upload_s3():
    result_dir = "./result_img"
    
    compare_file(result_dir) 
      
upload_s3()
   

    