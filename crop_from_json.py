import json
from PIL import Image
from pathlib import Path
from tqdm import tqdm

def read_bbox(json_pth: Path) -> list:
    anno = json.load(open(json_pth, 'r'))
    bbox_infos = anno['shapes']
    bbox_res = []
    for bbox in bbox_infos:
        coors = bbox['points']
        if (coors[0][0] < coors[1][0]):
            coors = (coors[0][0],
                    coors[0][1],
                    coors[1][0],
                    coors[1][1],)
        else:
            coors = (coors[1][0],
                    coors[1][1],
                    coors[0][0],
                    coors[0][1],)
        bbox_res.append(coors)
    
    return bbox_res

def main(root_dir: Path, save_dir: Path):
    if not save_dir.exists():
        save_dir.mkdir()

    image_list = list(root_dir.glob("*.tiff"))
    for image in tqdm(image_list):
        filename = Path(image).stem
        json_file = Path(str(image).replace('.tiff', '.json'))
        if not json_file.exists():
            continue
        save_prefix = save_dir / (str(filename) + 'out')
        
        img = Image.open(image)
        bboxes = read_bbox(json_file)

        for i, bbox in enumerate(bboxes):
            out = img.crop(bbox)  
            out.save(str(save_prefix) + '_' + str(i) + '.png')
    
if __name__ == "__main__":
    root = Path('/Users/shuyi/dataset/qddata/20230604/part1/defects_234')
    save = root / 'crop'
    main(root, save)
