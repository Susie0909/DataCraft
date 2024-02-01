# DataCraft
Data preprocessing for AI model 

## Splice

Splice several small images into a large image, to simulate the linear-array camera image.

### Prepare

The dir should be like:

```python
|--input_dir # small images & annotations
|   |--images 
|       |--img1.png
|       |--img2.png
|   |--labels # in YOLO format
|       |--anno1.txt
|       |--anno2.txt
|--output_dir # splicing result
|   |--images 
|       |--img1.tiff
|       |--img2.tiff
|   |--labels # in YOLO format
|       |--anno1.txt
|       |--anno2.txt

```

### Use

Change the paras, and run,

```shell
python splice.py /Users/dataset/yolo_crk_lkg_spl /Users/dataset/large_yolo_crk_lkg_spl 800 10 5

```


## Visualize

Visualize the annotations (YOLO format) for instance segmentation task.

### Prepare

The dir should be like:

```python
|--img_dir  # original images
|   |--img1.png
|   |--img2.png
|--anno_dir  # annotations
|   |--anno1.txt
|   |--anno2.txt
|--vis_anno  # the results
|   |--img1.png
|   |--img2.png

```

### Use

You should first change the path of img_dir and anno_dir, and then run this command:

```shell
python vis_txtlabel.py
```

The results will be saved in `vis_anno`