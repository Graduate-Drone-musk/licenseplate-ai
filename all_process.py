import os
import shutil
import glob

from LP_detection.detect import lp_detect
from crop import crop_img
from LP_ocr.demo import license_recognize

from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory

def set():
    return {
        "root": ROOT,
        "weight_path": ROOT / "LP_detection/runs/train/cd/weights/best.pt",
        "data":        ROOT / 'LP_detection/data/dataset.yaml',
        "result_path": ROOT / "result_img",
        "source":      ROOT / "DB_image"
    }

if __name__ == "__main__":
    setting = set()
    
    # Get Image to server
    setting["name"] = "first"
    
    # detect
    # lp_detect(setting)
    
    # Crop
    detect_result_path = setting["result_path"] / setting["name"]
    label_list = glob.glob(str(detect_result_path / 'labels')+'/*.txt')
    crop_img(setting, label_list)
    
    # crop to recognize
    license_recognize(setting)
    
    # 해야할 것
    # 두 개의 txt 파일 존재하는지 확인
    # 두 개의 txt 파일을 비교하여 같은 것이 있으면 가져오고 해당
    # 해당 파일 원본 전송 {날짜_시간_번호판}
    # 언제 삭제할지 고민해야함
    
    
    
    # 각 폴더에서 detect 진행
    # 연속으로 사용 불가: Out of memory
    # 따라서 한 곳에 모아 준 후 해야함
    # Get Image Folder in dir
    # folder_list = os.listdir(str(source_path))
    # 파일 옮기기
    # for folder in folder_list:
    #     file_list = glob.glob(str(source_path/folder/"*"))
    #     for file in file_list:
    #         name = file.split("\\")[-1]
    #         shutil.copy(file, str(input_path/name))
    
    
        
    
    