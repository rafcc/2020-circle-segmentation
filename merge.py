import argparse
import os, cv2
import numpy as np

def normalize_y(image):
    image = image/255
    return image

def load_Y(folder_path,s = "",no_flag = False):

    image_files = os.listdir(folder_path)
    image_files_new = []
    for file_name in image_files:
        if (no_flag == True):
            if(not ( "+" in file_name ) and not ("-" in file_name[-10]) ):
                image_files_new.append(file_name)
            continue
        if(s in file_name):
            image_files_new.append(file_name)


    image_files = image_files_new
    image_files.sort()
    images = []
    for i, image_file in enumerate(image_files):
        image = cv2.imread(folder_path + os.sep + image_file, cv2.IMREAD_GRAYSCALE)
        image = image[:, :, np.newaxis]
        images.append(normalize_y(image))
        print(image_file)
    return images

def denormalize_y(image):
    image = image*255
    return image


def merge_1(l, lm3, lm2, lm1, lp1, lp2, lp3, l_th, m_th):
    l_m = []  #label_merged
    for i in range(len(l)):
        l[i][l[i] >= l_th] = 1.0
        l[i][l[i] < l_th] = 0.0
        lm3[i][lm3[i] >= l_th] = 1.0
        lm3[i][lm3[i] < l_th] = 0.0
        lm2[i][lm2[i] >= l_th] = 1.0
        lm2[i][lm2[i] < l_th] = 0.0
        lm1[i][lm1[i] >= l_th] = 1.0
        lm1[i][lm1[i] < l_th] = 0.0
        lp1[i][lp1[i] >= l_th] = 1.0
        lp1[i][lp1[i] < l_th] = 0.0
        lp2[i][lp2[i] >= l_th] = 1.0
        lp2[i][lp2[i] < l_th] = 0.0
        lp3[i][lp3[i] >= l_th] = 1.0
        lp3[i][lp3[i] < l_th] = 0.0
 
        tmp = ( l[i] + lm3[i] + lm2[i] + lm1[i] + lp1[i] + lp2[i] + lp3[i] ) / 7.0
        tmp[tmp < m_th] = 0.0
        tmp[tmp >= m_th] = 1.0
        l_m.append(tmp)
    return l_m

def merge_2(l, lm3, lm2, lm1, lp1, lp2, lp3, m_th):
    l_m = []   #label_merged
    for i in range(len(l)):
        tmp = ( l[i] + lm3[i] + lm2[i] + lm1[i] + lp1[i] + lp2[i] + lp3[i] ) / 7.0
        tmp[tmp < m_th] = 0.0
        tmp[tmp >= m_th] = 1.0
        l_m.append(tmp)
    return l_m

def merge_3(l, lm3, lm2, lm1, lp1, lp2, lp3):
    l_m = []   #label_merged
    for i in range(len(l)):
        tmp = ( l[i] + lm3[i] + lm2[i] + lm1[i] + lp1[i] + lp2[i] + lp3[i] ) / 7.0
        l_m.append(tmp)
    return l_m

def save_file(l_m,image_path,save_path):
    image_files = os.listdir(image_path)
    image_files_new = []
    for file_name in image_files:
            if(not ( "+" in file_name ) and not ("-" in file_name[-10]) ):
                image_files_new.append(file_name)
    image_files = image_files_new
    image_files.sort()
    for i,file_path in enumerate(image_files):
         cv2.imwrite(save_path +"/"+ file_path, denormalize_y(l_m[i]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('-l' , '--label'   , type=str,  default='tmp', help='tmp')
    parser.add_argument('-m', '--label_merged'   , type=str,  default='tmp', help='tmp')
    parser.add_argument('-lth' , '--label_th'   , type=str,  default='tmp', help='tmp')
    parser.add_argument('-mth' , '--merge_th'   , type=str,  default='tmp', help='tmp')
    parser.add_argument('-flag', '--flag'  , type=str,  default='tmp', help='tmp')
    args = parser.parse_args()
    
    l = load_Y(args.label,no_flag = True)
    lm3 = load_Y(args.label, '_-3.')
    lm2 = load_Y(args.label, '_-2.')
    lm1 = load_Y(args.label, '_-1.')
    lp1 = load_Y(args.label, '_+1.')
    lp2 = load_Y(args.label, '_+2.')
    lp3 = load_Y(args.label, '_+3.')


    if args.flag == "one":
        l_m = merge_1(l, lm3, lm2, lm1, lp1, lp2, lp3, float(args.label_th),float(args.merge_th))  
    if args.flag == "two":
        l_m = merge_2(l, lm3, lm2, lm1, lp1, lp2, lp3, float(args.merge_th))  
    if args.flag == "three":
        l_m = merge_3(l, lm3, lm2, lm1, lp1, lp2, lp3)  

    save_file(l_m,args.label,args.label_merged)