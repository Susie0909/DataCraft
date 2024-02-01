import cv2
import os
from pathlib import Path
import numpy as np
import pdb
import glob
from tqdm import tqdm

def visTxt(img_path: str, anno_path: str):
    img = cv2.imread(img_path)
    with open(anno_path, 'r') as f:
        anno = f.readlines()
    img_size = img.shape[0]
    # points = []
    for obj in anno:
        obj_info = obj.strip().split(' ')
        coords = [int(float(ori_coords) * img_size) for ori_coords in obj_info[1:]]
        pts = []
        for i in range(0, len(coords), 2):
            pts.append([coords[i], coords[i + 1]])
            # pts = np.array([coords[i], coords[i + 1]], dtype=np.int32)
        pts = np.array(pts, dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
    # pts = np.array(points, dtype=np.int32)
    # pts = pts.reshape((-1, 1, 2))
    

    cv2.imwrite(img_path.replace("images", "vis_anno"), img)

if __name__ == '__main__':
    img_list = sorted(glob.glob("/Users/shuyi/Documents/dataset/0201/images/*"))
    anno_list = sorted(glob.glob("/Users/shuyi/Documents/dataset/0201/labels/*"))
    for i in tqdm(range(len(img_list))):
        visTxt(img_list[i], anno_list[i])