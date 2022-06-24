import boto3
import secret
import os
import glob

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
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    for file in file_list:
        file_path = file.split("\\")[7:]  
        s3.Bucket(bucket_name).upload_file(file, '/'.join(file_path))


if __name__ == "__main__":
    # s3 connect
    s3 = s3_res_connect()
    for bucket in s3.buckets.all():
        print(bucket.name)

    bucket_name = "licenseplateimg"
    
    result_img_path =ROOT/ "result_img"
    result_list = os.listdir(result_img_path)
    for r_path in result_list:
        file_path = result_img_path / r_path
        crop_text_files = glob.glob(str(file_path)+"/*/*")
        detectioin_files = glob.glob(str(file_path)+"/*.jpg")
        
        upload_files(s3, bucket_name, crop_text_files)
        upload_files(s3, bucket_name, detectioin_files)
