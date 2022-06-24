from unicodedata import decimal
import cv2
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

main_dir = 'C:\\Users\\parks\\Desktop\\대학\\4학년 1학기\\ml\\term_project'
def temp():
    car_loc_list = []
    with open(os.path.join(main_dir,'car.txt'), 'r') as f:
        locs = f.readlines()
        image = cv2.imread('.\\car.jpg')
        img_shape = image.shape
        le=0
        for loc in locs:
            loc = loc[2:-1]
            loc = loc.split()
            int_loc = list(map(float, loc))# X Y W H
            x = int(int_loc[0] * img_shape[1])
            w = int(int_loc[2] * img_shape[1])
            y = int(int_loc[1] * img_shape[0])
            h = int(int_loc[3] * img_shape[1])
            crop_img = image[y-h//2:y+h//2, x-w//2:x+w//2+1]
            print(crop_img.shape)
            cv2.imwrite('.\\crop_{}.jpg'.format(le) ,crop_img)
            le+=1
    # length = len(file)

# 
# data = np.array(data)
# cv2.imshow('0', image)

# cv2.waitKey(0)

def crop_img(setting, label_list):
    result_path = setting["result_path"] / setting["name"]
    crop_path = result_path / "crop"
    print(crop_path)
    if not os.path.isdir(crop_path):
        os.mkdir(crop_path)
    
    for label in label_list:
        with open(label, 'r') as f:
            name = label.split("\\")[-1].split(".")[0]
            locs = f.readlines()
            image = cv2.imread(str(setting["source"] / name) +'.jpg')
            img_shape = image.shape
            le=0
            for loc in locs:
                loc = loc[2:-1]
                loc = loc.split()
                int_loc = list(map(float, loc))# X Y W H
                x = int(int_loc[0] * img_shape[1])
                w = int(int_loc[2] * img_shape[1])
                y = int(int_loc[1] * img_shape[0])
                h = int(int_loc[3] * img_shape[1])
                crop_img = image[y-h//2:y+h//2, x-w//2:x+w//2+1]
                cv2.imwrite(crop_path /'{}_{}.jpg'.format(name,le) ,crop_img)
                le+=1