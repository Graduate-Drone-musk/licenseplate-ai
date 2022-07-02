import Generator_augmentation as gen_aug
import Generator_original as gen_ori
import Generator_perspective as gen_per

from pathlib import Path
import os
import sys

def save_txt(path, list):
    with open(os.path.join(path, "gt.txt"), 'a') as f:
        f.write('\n'.join(list))
        f.write("\n")

def make_img(gen, num_list, save_txt_path):
    gen.Type_new(num_list[0], save=save)
    print("Type new finish")
    gen.Type_0(num_list[1], save=save)
    print("Type 0 finish")
    gen.Type_1(num_list[2], save=save)
    print("Type 1 finish")
    gen.Type_2(num_list[3], save=save)
    print("Type 2 finish")
    gen.Type_3(num_list[4], save=save)
    print("Type 3 finish")
    gen.Type_4(num_list[5], save=save)
    print("Type 4 finish")
    gen.Type_5(num_list[6], save=save)
    print("Type 5 finish")
    
    save_txt(save_txt_path, gen.txt_list)




if __name__=="__main__":
    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[1]  # ROOT Dir

    save_dir = os.path.join(ROOT, "carplate_img")

    train_dir = os.path.join(save_dir, "training\\CI")
    train_img_dir = os.path.join(train_dir, "image")
    
    valid_dir = os.path.join(save_dir,"validation\\CI")
    valid_img_dir = os.path.join(valid_dir, "image")
    
    main_dir = os.path.join(ROOT, "custom_carplate")

    
    save = True
    cnt =0
    
    # train_data 만들기
    # Original
    train_ori = gen_ori.ImageGenerator(train_img_dir, main_dir, cnt=cnt)
    num_list = [400,20,20,20,250,250,40]
    make_img(train_ori, num_list, train_dir)
    cnt = train_ori.cnt
    
    # Augmentation
    train_aug = gen_aug.ImageGenerator(train_img_dir, main_dir, cnt=cnt)
    num_list = [400,20,20,20,250,250,40]
    make_img(train_aug, num_list, train_dir)
    cnt = train_aug.cnt
    
    # Perspective
    train_per = gen_per.ImageGenerator(train_img_dir, main_dir, cnt=cnt)
    num_list = [400,20,20,20,250,250,40]
    make_img(train_per, num_list, train_dir)
    cnt = train_per.cnt
    
    # valid_data 만들기
    # Original
    valid_ori = gen_ori.ImageGenerator(valid_img_dir, main_dir, cnt=cnt)
    num_list = [80,4,4,4,50,50,8]
    make_img(valid_ori, num_list, valid_dir)
    cnt = valid_ori.cnt
    
    # Augmentation
    valid_aug = gen_aug.ImageGenerator(valid_img_dir, main_dir, cnt=cnt)
    num_list = [80,4,4,4,50,50,8]
    make_img(valid_aug, num_list, valid_dir)
    cnt = valid_aug.cnt
    
    # Perspective
    valid_per = gen_per.ImageGenerator(valid_img_dir, main_dir, cnt=cnt)
    num_list = [80,4,4,4,50,50,8]
    make_img(valid_per, num_list, valid_dir)
    cnt = valid_per.cnt

    

    
    
