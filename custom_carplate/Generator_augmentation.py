import os, random
import cv2
import numpy as np
import argparse
from parameter import *

def image_augmentation(img, ang_range=6, shear_range=3, trans_range=3):
    # Rotation
    ang_rot = np.random.uniform(ang_range) - ang_range / 2
    rows, cols, ch = img.shape
    Rot_M = cv2.getRotationMatrix2D((cols / 2, rows / 2), ang_rot, 0.9)

    # Translation
    tr_x = trans_range * np.random.uniform() - trans_range / 2
    tr_y = trans_range * np.random.uniform() - trans_range / 2
    Trans_M = np.float32([[1, 0, tr_x], [0, 1, tr_y]])

    # Shear
    pts1 = np.float32([[5, 5], [20, 5], [5, 20]])

    pt1 = 5 + shear_range * np.random.uniform() - shear_range / 2
    pt2 = 20 + shear_range * np.random.uniform() - shear_range / 2
    pts2 = np.float32([[pt1, 5], [pt2, pt1], [5, pt2]])
    shear_M = cv2.getAffineTransform(pts1, pts2)

    img = cv2.warpAffine(img, Rot_M, (cols, rows))
    img = cv2.warpAffine(img, Trans_M, (cols, rows))
    img = cv2.warpAffine(img, shear_M, (cols, rows))

    # Brightness
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    img = np.array(img, dtype=np.float64)
    random_bright = .4 + np.random.uniform()
    img[:, :, 2] = img[:, :, 2] * random_bright
    img[:, :, 2][img[:, :, 2] > 255] = 255
    img = np.array(img, dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)

    # Blur
    blur_value = random.randint(0,5) * 2 + 1
    img = cv2.blur(img,(blur_value, blur_value))

    return img


class ImageGenerator:
    def __init__(self, save_path, main_path, cnt=0):
        self.save_path = save_path
        # self.save_path2 = "C:\\Users\\parks\\Desktop\\carplate_detect\\CRNN\\carplate\\training"
        
        # Plate
        self.plate = cv2.imread(os.path.join(main_path,"plate.jpg"))
        self.plate2 = cv2.imread(os.path.join(main_path,"plate_y.jpg"))
        self.plate3 = cv2.imread(os.path.join(main_path,"plate_g.jpg"))
        self.plate4 = cv2.imread(os.path.join(main_path,"plate_new.jpg"))

        # loading number
        self.number, self.number_list = self.load_data(main_path, "num")
        self.char,  self.char_list = self.load_data(main_path, "char1")
        
        # loading number ====================  yellow-two-line  ==========================
        self.number_y, _ = self.load_data(main_path, "num_y")
        self.char_y,  _ = self.load_data(main_path, "char1_y")
        
        self.resion_y, self.resion_list = self.load_data(main_path, "region_y")
        
        # loading number ====================  green-two-line  ==========================
        self.number_g, _ = self.load_data(main_path, "num_g")
        self.char_g,  _ = self.load_data(main_path, "char1_g")
       
        self.resion_g, _ = self.load_data(main_path, "region_g")
        
        self.cnt = cnt
        self.txt_list = []
    
        
    def load_data(self, main_path, inner_folder):
        """_summary_
            Args:
                main_path (string): path
                inner_folder (string) : inner path
        """
        # loading number or char
        file_path = os.path.join(main_path, inner_folder)
        file_list = os.listdir(file_path)
        data = list()
        data_list = list()
        for file in file_list:
            img_path = os.path.join(file_path, file)
            img = cv2.imread(img_path)
            data.append(img)
            data_list.append(file[0:-4])

        return data, data_list
    
    def Type_new(self, num, save=False):
        # 123가 4567
        h = 45; w = 80
        number = [cv2.resize(number, (h, w)) for number in self.number]
        char = [cv2.resize(char, (65, 70)) for char in self.char]

        for i in range(num):
            Plate = cv2.resize(self.plate4, (520, 110), interpolation=cv2.INTER_AREA)
            random_width = random.randint(140, 230)
            random_height = random.randint(550, 720)
            random_R, random_G, random_B = random.randint(0,255), random.randint(0,255), random.randint(0,255)
            background = np.zeros((random_width, random_height, 3), np.uint8)
            cv2.rectangle(background, (0, 0), (random_height, random_width), (random_R, random_G, random_B), -1)
            
            txt = ""
            label_en = ""
            # row -> y , col -> x
            row, col = 20, 80  # row + 83, col + 56    
            
            # number 1
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + w, col:col + h, :] = number[rand_int]
            col += h
            
            # number 2
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + w, col:col + h, :] = number[rand_int]
            col += h

            # number 3
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + w, col:col + h, :] = number[rand_int]
            col += h

            # character 3
            txt += KOREAN_PARAM[self.char_list[i%37]]
            label_en += self.char_list[i%37]
            Plate[row:row + 70, col:col + 65, :] = char[i%37]
            col += (65 + 25)

            # number 4
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + w, col:col + h, :] = number[rand_int]
            col += h

            # number 5
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + w, col:col + h, :] = number[rand_int]
            col += h

            # number 6
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + w, col:col + h, :] = number[rand_int]
            col += h

            # number 7
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + w, col:col + h, :] = number[rand_int]
            col += h
            
            random_w = random.randint(0, random_width - 110)
            random_h = random.randint(0, random_height - 520)
            background[random_w:110+random_w, random_h:520+random_h, :] = Plate
            background = image_augmentation(background)
            
            str_i = str(self.cnt)
            label = "image_" + '0' * (4-len(str_i)) + str_i
            self.cnt += 1
            if save:
                path = os.path.join(self.save_path, label + ".jpg")
                self.txt_list.append("{} {}".format(path,txt))
                cv2.imwrite(path, background)
                #cv2.imwrite(self.save_path2 + "\\{}".format(label_en) + ".jpg", Plate)
            else:
                cv2.imshow(label, background)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
    
    def Type_0(self, num, save=False):
        # 123가 4567
        h = 50; w = 80
        number = [cv2.resize(number, (h, w)) for number in self.number]
        char = [cv2.resize(char, (65, 70)) for char in self.char]

        for i in range(num):
            Plate = cv2.resize(self.plate, (520, 110), interpolation=cv2.INTER_AREA)
            random_width = random.randint(140, 230)
            random_height = random.randint(550, 720)
            random_R, random_G, random_B = random.randint(0,255), random.randint(0,255), random.randint(0,255)
            background = np.zeros((random_width, random_height, 3), np.uint8)
            cv2.rectangle(background, (0, 0), (random_height, random_width), (random_R, random_G, random_B), -1)
            
            txt = ""
            label_en = ""
            # row -> y , col -> x
            row, col = 20, 40  # row + 83, col + 56    
            
            # number 1
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + w, col:col + h, :] = number[rand_int]
            col += h
            
            # number 2
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + w, col:col + h, :] = number[rand_int]
            col += h

            # number 3
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + w, col:col + h, :] = number[rand_int]
            col += h

            # character 3
            txt += KOREAN_PARAM[self.char_list[i%37]]
            label_en += self.char_list[i%37]
            Plate[row:row + 70, col:col + 65, :] = char[i%37]
            col += (65 + 25)

            # number 4
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + w, col:col + h, :] = number[rand_int]
            col += h

            # number 5
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + w, col:col + h, :] = number[rand_int]
            col += h

            # number 6
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + w, col:col + h, :] = number[rand_int]
            col += h

            # number 7
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + w, col:col + h, :] = number[rand_int]
            col += h
            
            random_w = random.randint(0, random_width - 110)
            random_h = random.randint(0, random_height - 520)
            background[random_w:110+random_w, random_h:520+random_h, :] = Plate
            background = image_augmentation(background)
            
            str_i = str(self.cnt)
            label = "image_" + '0' * (4-len(str_i)) + str_i
            self.cnt += 1
            if save:
                path = os.path.join(self.save_path, label + ".jpg")
                self.txt_list.append("{} {}".format(path,txt))
                cv2.imwrite(path, background)
                #cv2.imwrite(self.save_path2 + "\\{}".format(label_en) + ".jpg", Plate)
            else:
                cv2.imshow(label, background)
                cv2.waitKey(0)
                cv2.destroyAllWindows()


    def Type_1(self, num, save=False):
        number = [cv2.resize(number, (56, 83)) for number in self.number]
        char = [cv2.resize(char1, (60, 83)) for char1 in self.char]

        for i in range(num):
            Plate = cv2.resize(self.plate, (520, 110))
            random_width = random.randint(140, 230)
            random_height = random.randint(550, 720)
            random_R, random_G, random_B = random.randint(0,255), random.randint(0,255), random.randint(0,255)
            background = np.zeros((random_width, random_height, 3), np.uint8)
            cv2.rectangle(background, (0, 0), (random_height, random_width), (random_R, random_G, random_B), -1)

            txt = ""
            label_en="Z"
            # row -> y , col -> x
            row, col = 13, 35  # row + 83, col + 56
            # number 1
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            col += 56

            # number 2
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            col += 56

            # character 3
            txt += KOREAN_PARAM[self.char_list[i%37]]
            label_en += self.char_list[i%37]
            Plate[row:row + 83, col:col + 60, :] = char[i%37]
            col += (60 + 36)

            # number 4
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            col += 56

            # number 5
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            col += 56

            # number 6
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            col += 56

            # number 7
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            col += 56

            random_w = random.randint(0, random_width - 110)
            random_h = random.randint(0, random_height - 520)
            background[random_w:110+random_w, random_h:520+random_h, :] = Plate
            background = image_augmentation(background)

            str_i = str(self.cnt)
            label = "image_" + '0' * (4-len(str_i)) + str_i
            self.cnt += 1
            
            if save:
                path = os.path.join(self.save_path, label + ".jpg")
                self.txt_list.append("{} {}".format(path,txt))
                cv2.imwrite(path, background)
                #cv2.imwrite(self.save_path2 + "\\{}".format(label_en) + ".jpg", Plate)
            else:
                cv2.imshow(label, background)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    def Type_2(self, num, save=False):
        number = [cv2.resize(number, (45, 83)) for number in self.number]
        char = [cv2.resize(char1, (49, 70)) for char1 in self.char]
        for i in range(num):
            Plate = cv2.resize(self.plate, (355, 155))
            random_width = random.randint(185, 275)
            random_height = random.randint(380, 555)
            random_R, random_G, random_B = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            background = np.zeros((random_width, random_height, 3), np.uint8)
            cv2.rectangle(background, (0, 0), (random_height, random_width), (random_R, random_G, random_B), -1)

            txt=""
            label_en="Z"
            row, col = 46, 10  # row + 83, col + 56

            # number 1
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 45, :] = number[rand_int]
            col += 45

            # number 2
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 45, :] = number[rand_int]
            col += 45

            # char 3
            txt += KOREAN_PARAM[self.char_list[i%37]]
            label_en += self.char_list[i%37]
            Plate[row + 12:row + 82, col + 2:col + 49 + 2, :] = char[i%37]
            col += 49 + 2

            # number 4
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 83, col + 2:col + 45 + 2, :] = number[rand_int]
            col += 45 + 2

            # number 5
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 45, :] = number[rand_int]
            col += 45

            # number 6
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 45, :] = number[rand_int]
            col += 45

            # number 7
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 45, :] = number[rand_int]
            col += 45

            random_w = random.randint(0, random_width - 155)
            random_h = random.randint(0, random_height - 355)
            background[random_w:155 + random_w, random_h:355 + random_h, :] = Plate
            background = image_augmentation(background)

            str_i = str(self.cnt)
            label = "image_" + '0' * (4-len(str_i)) + str_i
            self.cnt += 1
            
            if save:
                path = os.path.join(self.save_path, label + ".jpg")
                self.txt_list.append("{} {}".format(path,txt))
                cv2.imwrite(path, background)
            else:
                cv2.imshow(label, background)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    def Type_3(self, num, save=False):
        number1 = [cv2.resize(number, (44, 60)) for number in self.number_y]
        number2 = [cv2.resize(number, (64, 90)) for number in self.number_y]
        resion = [cv2.resize(resion, (88, 60)) for resion in self.resion_y]
        char = [cv2.resize(char1, (64, 62)) for char1 in self.char_y]

        for i in range(num):
            Plate = cv2.resize(self.plate2, (336, 170))
            random_width = random.randint(200, 290)
            random_height = random.randint(360, 536)
            random_R, random_G, random_B = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            background = np.zeros((random_width, random_height, 3), np.uint8)
            cv2.rectangle(background, (0, 0), (random_height, random_width), (random_R, random_G, random_B), -1)

            txt=""
            label_en=""
            # row -> y , col -> x
            row, col = 8, 76

            # resion
            txt += KOREAN_PARAM[self.resion_list[i % 16]]
            label_en += self.resion_list[i % 16]
            Plate[row:row + 60, col:col + 88, :] = resion[i % 16]
            col += 88 + 8

            # number 1
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 60, col:col + 44, :] = number1[rand_int]
            col += 44

            # number 2
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 60, col:col + 44, :] = number1[rand_int]

            row, col = 72, 8

            # character 3
            txt += KOREAN_PARAM[self.char_list[i%37]]
            label_en += self.char_list[i%37]
            Plate[row:row + 62, col:col + 64, :] = char[i % 37]
            col += 64

            # number 4
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            col += 64

            # number 5
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            col += 64

            # number 6
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            col += 64

            # number 7
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]

            s_width, s_height = int((random_width - 170) / 2), int((random_height - 336) / 2)
            background[s_width:170 + s_width, s_height:336 + s_height, :] = Plate
            background = image_augmentation(background)
            
            str_i = str(self.cnt)
            label = "image_" + '0' * (4-len(str_i)) + str_i
            self.cnt += 1

            if save:
                path = os.path.join(self.save_path, label + ".jpg")
                self.txt_list.append("{} {}".format(path,txt))
                cv2.imwrite(path, background)
                #cv2.imwrite(self.save_path2 + "\\{}".format(label_en) + ".jpg", Plate)
            else:
                cv2.imshow(label, background)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    def Type_4(self, num, save=False):
        number1 = [cv2.resize(number, (44, 60)) for number in self.number_g]
        number2 = [cv2.resize(number, (64, 90)) for number in self.number_g]
        resion = [cv2.resize(resion, (88, 60)) for resion in self.resion_g]
        char = [cv2.resize(char1, (64, 62)) for char1 in self.char_g]

        for i in range(num):
            Plate = cv2.resize(self.plate3, (336, 170))
            random_width = random.randint(200, 290)
            random_height = random.randint(360, 536)
            random_R, random_G, random_B = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            background = np.zeros((random_width, random_height, 3), np.uint8)
            cv2.rectangle(background, (0, 0), (random_height, random_width), (random_R, random_G, random_B), -1)

            txt = ""
            label_en=""
            # row -> y , col -> x
            row, col = 8, 76

            # resion
            txt += KOREAN_PARAM[self.resion_list[i % 16]]
            label_en += self.resion_list[i % 16]
            Plate[row:row + 60, col:col + 88, :] = resion[i % 16]
            col += 88 + 8

            # number 1
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 60, col:col + 44, :] = number1[rand_int]
            col += 44

            # number 2
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 60, col:col + 44, :] = number1[rand_int]

            row, col = 72, 8

            # character 3
            txt += KOREAN_PARAM[self.char_list[i%37]]
            label_en += self.char_list[i%37]
            Plate[row:row + 62, col:col + 64, :] = char[i % 37]
            col += 64

            # number 4
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            col += 64

            # number 5
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            col += 64

            # number 6
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            col += 64

            # number 7
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]

            s_width, s_height = int((random_width - 170) / 2), int((random_height - 336) / 2)
            background[s_width:170 + s_width, s_height:336 + s_height, :] = Plate
            background = image_augmentation(background)
            
            str_i = str(self.cnt)
            label = "image_" + '0' * (4-len(str_i)) + str_i
            self.cnt += 1

            if save:
                path = os.path.join(self.save_path, label + ".jpg")
                self.txt_list.append("{} {}".format(path,txt))
                cv2.imwrite(path, background)
                #cv2.imwrite(self.save_path2 + "\\{}".format(label_en) + ".jpg", Plate)
            else:
                cv2.imshow(label, background)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    def Type_5(self, num, save=False):
        number1 = [cv2.resize(number, (60, 65)) for number in self.number_g]
        number2 = [cv2.resize(number, (80, 90)) for number in self.number_g]
        char = [cv2.resize(char1, (60, 65)) for char1 in self.char_g]

        for i in range(num):
            Plate = cv2.resize(self.plate3, (336, 170))
            random_width = random.randint(200, 290)
            random_height = random.randint(360, 536)
            random_R, random_G, random_B = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            background = np.zeros((random_width, random_height, 3), np.uint8)
            cv2.rectangle(background, (0, 0), (random_height, random_width), (random_R, random_G, random_B), -1)
            
            
            txt = ""
            label_en = "Z"
            # row -> y , col -> x
            row, col = 8, 78

            # number 1
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 65, col:col + 60, :] = number1[rand_int]
            col += 60

            # number 2
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 65, col:col + 60, :] = number1[rand_int]
            col += 60

            # character 3
            txt += KOREAN_PARAM[self.char_list[i%37]]
            label_en += self.char_list[i%37]
            Plate[row:row + 65, col:col + 60, :] = char[i%37]
            row, col = 75, 8

            # number 4
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 90, col:col + 80, :] = number2[rand_int]
            col += 80


            # number 5
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 90, col:col + 80, :] = number2[rand_int]
            col += 80

            # number 6
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 90, col:col + 80, :] = number2[rand_int]
            col += 80

            # number 7
            rand_int = random.randint(0, 9)
            txt += str(rand_int)
            label_en += self.number_list[rand_int]
            Plate[row:row + 90, col:col + 80, :] = number2[rand_int]

            random_w = random.randint(0, random_width - 170)
            random_h = random.randint(0, random_height - 336)
            background[random_w:170 + random_w, random_h:336 + random_h, :] = Plate

            background = image_augmentation(background)

            str_i = str(self.cnt)
            label = "image_" + '0' * (4-len(str_i)) + str_i
            self.cnt += 1
            
            if save:
                path = os.path.join(self.save_path, label + ".jpg")
                self.txt_list.append("{} {}".format(path,txt))
                cv2.imwrite(path, background)
                #cv2.imwrite(self.save_path2 + "\\{}".format(label_en) + ".jpg", Plate)
            else:
                cv2.imshow(label, background)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

if __name__=="__main__":
    crnn_path = "C:\\Users\\parks\\Desktop\\carplate_detect\\CRNN"

    save_dir = os.path.join(crnn_path, "image")
    main_dir = os.path.join(crnn_path, "Korean-license-plate-Generator")

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--img_dir", help="save image directory",
                        type=str, default=save_dir)
    parser.add_argument("-n", "--num", help="number of image",
                        type=int, default=1)
    parser.add_argument("-s", "--save", help="save or imshow",
                        type=bool, default=True)
    args = parser.parse_args()


    img_dir = args.img_dir

    A = ImageGenerator(img_dir, main_dir, cnt=750)

    num_img = args.num
    save = args.save

    cnt = 0
    file_list = []

    num_img = 40
    A.Type_new(num_img, save=save)
    print("Type new finish")
    A.Type_0(num_img, save=save)
    print("Type 0 finish")
    A.Type_1(num_img, save=save)
    print("Type 1 finish")
    A.Type_2(num_img, save=save)
    print("Type 2 finish")

    num_img = 10
    A.Type_3(num_img, save=save)
    print("Type 3 finish")
    A.Type_4(num_img, save=save)
    print("Type 4 finish")
    A.Type_5(num_img, save=save)
    print("Type 5 finish")
    print(os.path.join(crnn_path, "label"))
    print(A.cnt)
    with open(os.path.join(crnn_path, "label\\gt.txt"), 'a') as f:
        f.write('\n'.join(A.txt_list))
        f.write("\n")