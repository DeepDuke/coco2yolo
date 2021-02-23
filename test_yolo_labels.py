"""
Test yolo txt label
Author: @deepduke
"""
import os 
import cv2 
import matplotlib
import random


classes_names = ['bottle', 'fork', 'knife', 'spoon', 'banana', 'apple', 'orange', 'broccoli', 'carrot', 'hot dog', 'clock', 'scissors', 'toothbrush',
                 'frisbee', 'sports ball', 'wine glass', 'cup', 'bowl', 'sandwich', 'pizza', 'donut', 'cake', 'cell phone', 'book', 'mouse', 'remote'] 


def color_list():
    # Return first 10 plt colors as (r,g,b) https://stackoverflow.com/questions/51350872/python-from-color-name-to-rgb
    def hex2rgb(h):
        return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))

    return [hex2rgb(h) for h in matplotlib.colors.TABLEAU_COLORS.values()]  # or BASE_ (8), CSS4_ (148), XKCD_ (949)


def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


if __name__ == '__main__':

    colors = color_list()

    img_path = "/home/hazawa/COCO/images/val2017/"
    txt_path = "/home/hazawa/COCO/labels/val2017/"

    img_list = os.listdir(img_path)

    for img_file in img_list:
        img = cv2.imread(img_path + img_file)
        [H, W, C] = img.shape
        label_strs = None
        with open(txt_path + img_file.split('.')[0] + '.txt', 'r') as f:
            label_strs = f.readlines()
        label_strs = [ele.split(' ') for ele in label_strs]
        labels = [[int(label_str[0]), W*float(label_str[1]), H*float(label_str[2]), W*float(label_str[3]), H*float(label_str[4])] for label_str in label_strs]
        xyxy_bboxes = [[label[0], label[1]-label[3]/2.0, label[2]-label[4]/2.0, label[1]+label[3]/2.0, label[2]+label[4]/2.0] for label in labels]
        # draw each bbox
        for xyxy_bbox in xyxy_bboxes:
            color = colors[xyxy_bbox[0]%10]
            plot_one_box(xyxy_bbox[1:], img, color=color, label=classes_names[xyxy_bbox[0]])
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
