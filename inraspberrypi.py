import boto3
import secret
import os
import glob
import time
from pathlib import Path


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory

# file name = IP_현재시간 / 여러 이미지

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
    else:
        return s3

def upload_files(s3, bucket_name, file_list):
    root_dir = "main/"
    
    for file in file_list:
        file_path = file.split("\\")[7:]  
        s3.Bucket(bucket_name).upload_file(file, root_dir + '/'.join(file_path))

def file_exist(s3, bucket_name, prefix, fileN):
    for object in s3.Bucket(bucket_name).objects.filter(Prefix=prefix):
        print(object.key)
    
    for object in s3.Bucket(bucket_name).objects.filter(Prefix=prefix):
        if object.key.split("/")[-1] == fileN:
            return object.get()["Body"].read().decode('utf-8')
    return ""


def get_today():
    now = time.localtime(time.time()) 
    now_year = str(now.tm_year)
    now_month = '0'+str(now.tm_mon) if now.tm_mon//10==0 else str(now.tm_mon) 
    now_day =  '0'+str(now.tm_mday) if now.tm_mday//10==0 else str(now.tm_mday)
    return now_year + now_month + now_day
    
    
def upload_img():
    # Test
    ## S3 connect
    s3 = s3_res_connect()
    bucket_name = "licenseplateimg"
    
    ## 라즈베리파이의 Path 설정
    upload_img_path =ROOT/ "DB_image"

    today_name = get_today()
    upload_path =upload_img_path/ today_name # DB_image/20220621
    print(upload_path)
    upload_list =  os.listdir(upload_path)   # DB_image/20220621/*
    print(upload_list)
    have_upload = False
    
    # S3 Path
    s3_main_dir = "main/"+today_name
    
    # s3에 check파일 있는지에 따른 동작
    # aws s3에 check 파일
    check_txt="check.txt"
    folder_path = 'main/'+ "{}/".format(today_name)
    
    # txt 파일 내용
    txt_file = file_exist(s3, bucket_name, folder_path, check_txt)
    print(txt_file)
    new_data = []
    
    if txt_file != "":
        print(txt_file)
        txt_list = txt_file.split("\n")
        for file in upload_list:
            if file not in txt_list:
                new_data.append(file)
        txt_list = txt_list + new_data
        txt_list.sort()

        if new_data:
            s3.Object(bucket_name, s3_main_dir + "/check.txt").put(Body='\n'.join(txt_list))
            have_upload = True
    else:
        # Check.txt 파일 없을 때 
        new_data = upload_list
        print("d",new_data)
        s3.Object(bucket_name, s3_main_dir + "/check.txt").put(Body='\n'.join(new_data))
        have_upload = True
        
    
    if have_upload:
        for folder in new_data:
            file_path = upload_path / folder
            jpg_files = glob.glob(str(file_path)+"/*.jpg")
            upload_files(s3, bucket_name, jpg_files)   
    
if __name__ == "__main__":
    upload_img()        
