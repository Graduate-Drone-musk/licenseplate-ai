from LP_ocr import create_lmdb_dataset

import os    
import glob
import numpy as np
import cv2
import hashlib
import struct
from pathlib import Path

def encode_kor(path):
    img_array = np.fromfile(path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return cv2.imencode('.jpg', img)

def sub_name(path):
    name = path.split("\\")[-1].split(".")[0] # Only name
    name = name.split("-")[0]
    return name+".jpg"

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

if __name__ == '__main__':
    # CI = Custom Image RI = Real Image
    # fire.Fire(createDataset)
    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[0]  # root directory
    
    carplate_dir =  ROOT / 'carplate_img'
    lmdb_dir= ROOT / "lmdb"
    train_dir = os.path.join(carplate_dir, "training")
    valid_dir = os.path.join(carplate_dir, "validation")
    
    ci_path = os.path.join(train_dir, "CI")
    input_path = ci_path
    gtFile = os.path.join(ci_path, "gt.txt")
    outputPath = os.path.join(lmdb_dir, 'training')
    create_lmdb_dataset.createDataset(inputPath=input_path, gtFile=gtFile, outputPath=os.path.join(outputPath, "CI")) # train CI
    
    ri_path = os.path.join(train_dir, "RI")
    input_path = ri_path
    gtFile = os.path.join(ri_path, "gt.txt")
    create_lmdb_dataset.createDataset(inputPath=input_path, gtFile=gtFile, outputPath=os.path.join(outputPath, "RI")) # train RI
    
    ci_path = os.path.join(valid_dir, "CI")
    input_path = ci_path
    gtFile = os.path.join(ci_path, "gt.txt")
    outputPath = os.path.join(lmdb_dir, 'validation')
    create_lmdb_dataset.createDataset(inputPath=input_path, gtFile=gtFile, outputPath=os.path.join(outputPath, "CI")) # valid CI
    
    ri_path = os.path.join(valid_dir, "RI")
    input_path = ri_path
    gtFile = os.path.join(ri_path, "gt.txt")
    create_lmdb_dataset.createDataset(inputPath=input_path, gtFile=gtFile, outputPath=os.path.join(outputPath, "RI")) # valid RI