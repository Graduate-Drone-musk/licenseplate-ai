from unicodedata import decimal
import cv2
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

main_dir = 'C:\\Users\\parks\\Desktop\\대학\\4학년 1학기\\ml\\term_project'

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
