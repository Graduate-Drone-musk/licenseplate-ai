import boto3
import botocore
import secret
import time
import os
import glob

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

def file_exist(s3, bucket_name, prefix, local):
    key_name = []
    for object in s3.Bucket(bucket_name).objects.filter(Prefix=prefix):
        name = object.key.split("/")[2]
        if name not in local:
            key_name.append(object.key)   
    return key_name

# 오늘 날짜
def get_today():
    now = time.localtime(time.time()) 
    now_year = str(now.tm_year)
    now_month = '0'+str(now.tm_mon) if now.tm_mon//10==0 else str(now.tm_mon) 
    now_day =  '0'+str(now.tm_mday) if now.tm_mday//10==0 else str(now.tm_mday)
    return now_year + now_month + now_day        

# txt 내용 불러오기
def check(s3, bucket_name, prefix):
    for object in s3.Bucket(bucket_name).objects.filter(Prefix=prefix):
        if object.key.split("/")[-1] == 'check.txt':
            return object.get()["Body"].read().decode('utf-8')
    return ""



# 이미지 다운로드, txt 내용과 비교하여 없는 것만 가져오기
def download_s3(s3,bucket_name, today_name):
    new_folder_list = []
    
    check_txt = "check.txt"
    folder_path = 'main/'+ "{}/".format(today_name)
    
    path = "./DB_image/"+today_name
    local_dir = os.listdir(path)
    
    # txt 파일 내용
    key_name = file_exist(s3, bucket_name,  folder_path, local_dir)
   
    txt_contents = check(s3, bucket_name, folder_path)  # check.txt 내용
    txt_contents = txt_contents.split("\n")             # check.txt 내용 분리 

    for img_name in key_name:
        compare_exist = img_name.split("/")[2]
        if compare_exist in txt_contents :
            temp = img_name.split("/")[2]
            directory = f"{path}/{temp}"          # main/20220622/215207465_01234_56789
            os.makedirs(directory, exist_ok = True) 
        
            jpg_name = img_name.split("/")[-1]  # 이미지 객체 이름
            try:
                new_folder_list.append(directory)
                s3.Bucket(bucket_name).download_file(img_name, os.path.join(directory, jpg_name))   # directory 경로에 이미지 다운로드
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                else:
                    raise
    new_folder_list = list(set(new_folder_list))
    return new_folder_list

        
if __name__ == "__main__":
    # s3 connect
    s3 = s3_res_connect()
    bucket_name = "licenseplateimg"
    today_name = get_today()
    # check_txt = "check.txt"
    # folder_path = 'main/'+ "{}/".format(today_name)
    
    # # txt 파일 내용
    # key_name = file_exist(s3, bucket_name, folder_path, check_txt)
    
    # txt_contents = check(s3, bucket_name, folder_path)  # check.txt 내용
    # txt_contents = txt_contents.split("\n")             # check.txt 내용 분리 
    # print(txt_contents)
    download_s3(s3, bucket_name, today_name)