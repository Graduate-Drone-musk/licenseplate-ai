import os
import shutil
import glob
import time
import donwload_s3

from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory

# from LP_detection import detect
import LP_ocr.demo
import LP_detection.detect
# from LP_ocr import demo

from crop import crop_img

def set():
    return {
        "root": ROOT,
        "weight_path": ROOT / "LP_detection/runs/train/cd/weights/best.pt",
        "data":        ROOT / 'LP_detection/data/dataset.yaml',
        "result_path": ROOT / "result_img",
        "name": "temp"
    }

def get_today():
    now = time.localtime(time.time()) 
    now_year = str(now.tm_year)
    now_month = '0'+str(now.tm_mon) if now.tm_mon//10==0 else str(now.tm_mon) 
    now_day =  '0'+str(now.tm_mday) if now.tm_mday//10==0 else str(now.tm_mday)
    return now_year + now_month + now_day

if __name__ == "__main__":
    # s3 connect
    s3 = donwload_s3.s3_res_connect()
    s3_bucket_name = "licenseplateimg"
    day = get_today()
    
    # download
    donw_path = donwload_s3.download_s3(s3, s3_bucket_name, day)

    setting = set()
    # setting["name"] = get_today()
    
    
    # DB_image\20220621
    source = ROOT / "DB_image" / day
    if not os.path.isdir(source):
        os.mkdir(source)
    
    db_list = os.listdir(source)
        
    result_path = setting["result_path"] / setting["name"]
    done_list = []
    if os.path.isdir(result_path):
        done_list = os.listdir(result_path)
    
    todo_process=[]
    for db in db_list:
        if db not in done_list:
            todo_process.append(db)
            
    setting["source"] = ROOT/ "temp_img"
    if not os.path.isdir(setting["source"]):
        os.mkdir(setting["source"])
    
    
    temp_list = {}
    for todo in todo_process:
        # print(str(source)+"/"+todo+"/*.jpg")
        temp_list[todo] = []
        for jpg in glob.glob(str(source)+"\\"+todo+"/*.jpg"):
            temp_list[todo].append(jpg.split("\\")[-1])
            shutil.copy(jpg, setting["source"])
    
    # detect
    LP_detection.detect.lp_detect(setting)
    
    # Crop
    detect_result_path = setting["result_path"] / setting["name"]
    label_list = glob.glob(str(detect_result_path / 'labels')+'/*.txt')
    crop_img(setting, label_list)

    # crop to recognize
    LP_ocr.demo.license_recognize(setting)
    
    # 다시 분리
    result =  setting["result_path"] / day
    if not os.path.isdir(result):
        os.mkdir(result)
    
    # label 값 읽기
    with open(detect_result_path/'crop'/'result.txt', 'r', encoding='cp949') as f:
        recognize_list = f.readlines()

    for path, file_list in temp_list.items():
        split_path = result / path
        crop_folder = split_path / "crop"
        
        # 폴더 만들어 주고
        if not os.path.isdir(split_path):
            os.mkdir(split_path)
            
        # 내부 Crop 폴더 만들어 주고
        if not os.path.isdir(crop_folder):
            os.mkdir(crop_folder)
            
        # recog result
        recog_result = []
        
        # 라벨 값
        for file in file_list:
            f_name = file.split(".")[0]
            origin_crop = detect_result_path/'crop'/ f_name
            
            # re.write(f'{img_name} {pred}\n')
            
            # Crop 파일
            for c in glob.glob(str(origin_crop)+"_*.jpg"):
                c_name = c.split("\\")[-1]
                shutil.copy(c, crop_folder/c_name)    
            
            # detection 파일
            shutil.copy(detect_result_path/file, split_path/file)  
            
            # recognize 파일
            for string in recognize_list:
                p, r = string.split(" ")
                # print(p, name)
                if f_name in p:
                    p = split_path / p.split("\\")[-1]
                    string = "{} {}".format(p,r)
                    recog_result.append(string)
        
        with open(crop_folder / 'result.txt', 'w', encoding='utf-8') as f:
            f.write(''.join(recog_result))
    
    # Delete all file
    shutil.rmtree(detect_result_path)
    shutil.rmtree(setting["source"])
    exit()
    
    # 해야할 것
    # 두 개의 txt 파일 존재하는지 확인
    # 두 개의 txt 파일을 비교하여 같은 것이 있으면 가져오고 해당
    # 해당 파일 원본 전송 {날짜_시간_번호판}
    # 언제 삭제할지 고민해야함
    
    
    
        
    
    