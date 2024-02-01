"""
本脚本用于将带标注的小图像拼接成大图像。包括图像拼接和相应gt标注的修改。

文件目录结构
|--input_dir # 小图像目录
|   |--images # 小图像
|       |--img1.png
|       |--img2.png
|   |--labels # 对应gt真值，yolo格式
|       |--anno1.txt
|       |--anno2.txt
|--output_dir # 拼接后的大图像目录
|   |--images # 大图像
|       |--img1.tiff
|       |--img2.tiff
|   |--labels # 对应gt真值
|       |--anno1.txt
|       |--anno2.txt

参数：
input_dir：小图像及其标注文件路径
output_dir：新大图图像及标注文件路径
img_size：小图像尺寸 (默认800)
splice_num：水平/纵向方向，拼接个数
output_num：生成的大图数量
"""

from PIL import Image
from pathlib import Path
import random
import numpy as np
import argparse
from tqdm import tqdm
import os
import glob
import pdb

def main(args):
    input = Path(args.input_dir)
    output = Path(args.output_dir)
    img_size = args.img_size
    spl_num = args.splice_num
    output_num = args.output_num
    
    imgs_path = input / "images" / "train"
    annos_path = input / "labels" / "train"
    imgs_list = sorted(glob.glob(f"{imgs_path}/*"))
    annos_list = sorted(glob.glob(f"{annos_path}/*"))

    for ind in tqdm(range(output_num)):
        # 初始化大图
        outImg_size = spl_num * img_size
        outImg = Image.fromarray(np.zeros((outImg_size, outImg_size), dtype=np.uint8), "L")
        
        # 初始化gt
        outAnno = ""
        
        # 拼接大图，并转换gt
        for row in range(spl_num):
            for col in range(spl_num):
                ## load图像及gt
                img_id = random.randint(0, len(imgs_list) - 1) # 随机选一张小图像
                srcImg = Image.open(imgs_list[img_id])

                while (srcImg.size != (800, 800)):
                    img_id = random.randint(0, len(imgs_list) - 1) # 随机选一张小图像
                    srcImg = Image.open(imgs_list[img_id])

                anno = annos_list[img_id]
                with open(anno, 'r') as f:
                    anno_info = f.readlines()
                
                trans_x = col * img_size
                trans_y = row * img_size

                ## 转换图像
                outImg.paste(srcImg, (trans_x, trans_y))

                ## 转换gt
                for obj in anno_info:
                    obj_info = obj.strip().split(' ')
                    cls_id = obj_info[0]
                    coords = np.array([float(ori_coords) * img_size for ori_coords in obj_info[1:]])
                    for i in range(0, len(coords), 2):
                        coords[i] = (coords[i] + trans_x) / float(outImg_size)
                        coords[i + 1] = (coords[i + 1] + trans_y) / float(outImg_size)
                        # pdb.set_trace()
                    outAnno += cls_id + " " + " ".join([str(x) for x in coords]) + "\n"
        
        # 保存图像及gt
        if not Path(output / "images").exists():
            Path(output / "images").mkdir()
        if not Path(output / "labels").exists():
            Path(output / "labels").mkdir()
        outImg.save(output / "images" / f"{ind}.tiff")
        with open(output / "labels" / f"{ind}.txt" , "w") as f:
            f.write(outAnno)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type = str)
    parser.add_argument("output_dir", type = str)
    parser.add_argument("img_size", type = int)
    parser.add_argument("splice_num", type = int)
    parser.add_argument("output_num", type = int)
    args = parser.parse_args()

    
    main(args)
            
