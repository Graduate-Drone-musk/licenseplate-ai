import os
import cv2
import glob
import numpy as np
import hashlib
import struct
from pathlib import Path
import sys


"""_summary_
    CRNN을 위한 데이터 5000개 뽑아오기
    main_dir + Training + crnn_image
"""

def encode_kor(path):
    img_array = np.fromfile(path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return cv2.imencode('.jpg', img)

def sub_name(name):
    name = name[:-4]
    name = name.split("-")[0]
    return name

def split_train_test_set(path, test_ratio):
    byte = 8
    rate = test_ratio * 2**(byte*8)
    
    train_path = os.path.join(path, "crnn_train")
    test_path = os.path.join(path, "crnn_test")
    

    for img_path in glob.glob(path+"\\*.jpg"):
        # sub name
        name = sub_name(img_path)
        # encode
        result, encoded_img = encode_kor(img_path)
            
        if result:
            hash = hashlib.sha256(name.encode())
            unpack = float(struct.unpack('Q', hash.digest()[:byte])[0])
            if unpack < rate: # test set
                with open(os.path.join(test_path,name), mode='w+b') as f:
                    encoded_img.tofile(f)
            else: # train_set
                with open(os.path.join(train_path,name), mode='w+b') as f:
                    encoded_img.tofile(f)
            


if __name__=="__main__":
    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[1]  # YOLOv5 root directory

    ori_img_path = ROOT / 'dataset\\Training\\ocr_image\\ocr_data'
    ori_img_valid = ROOT / 'dataset\\Validation\\ocr_data'
    li = os.listdir(ori_img_path)
    valid_li = os.listdir(ori_img_valid)
    
    img_main_dir = ROOT / 'carplate_img'
    train_ri_dir = os.path.join(img_main_dir, "training\\RI")
    train_ri_image = os.path.join(train_ri_dir, "image")
    
    valid_ri_dir = os.path.join(img_main_dir, "validation\\RI")
    valid_ri_image = os.path.join(valid_ri_dir, "image")
    print(len(li))
    print(len(valid_li))
    
    result_train = []
    result_valid = []
    cnt = 0
    
    temp1 = 0
    temp2 = 0
    for index, name in enumerate(li):
        if index % 8 == 0: # 80000 / 8 : 10000
            temp1+=1   
            img_array = np.fromfile(os.path.join(ori_img_path, name), np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            cnt_str = str(cnt)
            new_name = "image_" + '0' * (4-len(cnt_str)) + cnt_str +".jpg"
            
            path = os.path.join(train_ri_image, new_name)
            cnt += 1
            
            cv2.imwrite(path, img)
            name = sub_name(name)
            result_train.append("{} {}".format(path, name))

    for index, name in enumerate(valid_li):
        if index % 20 == 0: # 10000 / 10 : 1000
            temp2 += 1
            img_array = np.fromfile(os.path.join(ori_img_valid, name), np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            cnt_str = str(cnt)
            new_name = "image_" + '0' * (4-len(cnt_str)) + cnt_str +".jpg"
            
            path = os.path.join(valid_ri_image, new_name)
            cnt += 1
            
            cv2.imwrite(path, img)
            name = sub_name(name)
            result_valid.append("{} {}".format(path, name))       
    print(temp1, temp2)
    with open(train_ri_dir+"\\gt.txt", 'w') as f:
        f.write('\n'.join(result_train))
        
    with open(valid_ri_dir+"\\gt.txt", 'w') as f:
        f.write('\n'.join(result_valid))
