import argparse
import os, cv2
import numpy as np

def normalize_y(image):
    image = image/255
    return image

def load_Y(folder_path):

    image_files = os.listdir(folder_path)
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


def proposed_1(c,c_in,c_out,c_th,c_in_th,c_out_th):
    c_p = []
    for i in range(len(c)):
        c[i][c[i] >= c_th] = 1.0
        c[i][c[i] < c_th] = 0.0
        c_in[i][c_in[i] >= c_in_th] = 1.0
        c_in[i][c_in[i] < c_in_th] = 0.0
        c_out[i][c_out[i] >= c_out_th]  = 1.0
        c_out[i][c_out[i] < c_out_th]  = 0.0    
        tmp = c_out[i] - c_in[i]
        tmp[tmp < 0.0] = 0.0
        c_p_tmp = c[i] + tmp
        c_p_tmp[c_p_tmp > 1.0] = 1.0
        c_p.append(c_p_tmp)
    return c_p

def proposed_2(c,c_in,c_out,c_th,c_in_th,c_out_th):
    c_p = []
    for i in range(len(c)):
        c[i][c[i] >= c_th] = 1.0
        c[i][c[i] < c_th] = 0.0
        c_in[i][c_in[i] >= c_in_th] = 1.0
        c_in[i][c_in[i] < c_in_th] = 0.0
        c_out[i][c_out[i] >= c_out_th]  = 1.0
        c_out[i][c_out[i] < c_out_th]  = 0.0
        tmp = c_out[i] + c[i]
        tmp[tmp > 1.0] = 1.0
        c_p_tmp = tmp - c_in[i]
        c_p_tmp[c_p_tmp < 0.0] = 0.0
        c_p.append(c_p_tmp)
    return c_p

def save_file(c_p,image_path,save_path):
    image_files = os.listdir(image_path)
    image_files.sort()
    for i,file_path in enumerate(image_files):
         cv2.imwrite(save_path +"/"+ file_path, denormalize_y(c_p[i]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('-c' , '--circle'   , type=str,  default='tmp', help='tmp')
    parser.add_argument('-i' , '--circle_in'   , type=str,  default='tmp', help='tmp')
    parser.add_argument('-o', '--circle_out'    , type=str,  default='tmp', help='tmp')
    parser.add_argument('-p', '--circle_proposed'   , type=str,  default='tmp', help='tmp')
    parser.add_argument('-c_th' , '--c_th'   , type=str,  default='tmp', help='tmp')
    parser.add_argument('-in_th' , '--in_th'   , type=str,  default='tmp', help='tmp')
    parser.add_argument('-out_th', '--out_th'    , type=str,  default='tmp', help='tmp')
    parser.add_argument('-flag', '--flag'    , type=str,  default='tmp', help='tmp')
    args = parser.parse_args()
    
    c = load_Y(args.circle)
    c_in = load_Y(args.circle_in)
    c_out = load_Y(args.circle_out)
    if args.flag == "one":
        c_p = proposed_1(c,c_in,c_out,float(args.c_th),float(args.in_th),float(args.out_th))  
    if args.flag == "two":
        c_p = proposed_2(c,c_in,c_out,float(args.c_th),float(args.in_th),float(args.out_th))

    save_file(c_p,args.circle,args.circle_proposed)
    







