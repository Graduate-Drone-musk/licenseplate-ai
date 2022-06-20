import boto3
import secret
import time
from pathlib import Path
import os

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



if __name__ == "__main__":
    # s3 connect
    s3 = s3_res_connect()
    for bucket in s3.buckets.all():
        print(bucket.name)

    result_img_path =ROOT/ "result_img"
    result_list = os.listdir(result_img_path)
    for r_path in result_list:
        print()
    pass
