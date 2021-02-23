"""
Convert voc xml label to yolo label
"""
import copy
from lxml.etree import Element, SubElement, tostring, ElementTree
 
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

classes_names = ['bottle', 'fork', 'knife', 'spoon', 'banana', 'apple', 'orange', 'broccoli', 'carrot', 'hot dog', 'clock', 'scissors', 'toothbrush',
                 'frisbee', 'sports ball', 'wine glass', 'cup', 'bowl', 'sandwich', 'pizza', 'donut', 'cake', 'cell phone', 'book', 'mouse', 'remote'] 

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


if __name__ == "__main__":
    train_xml_path = "./COCO/annotations/train2017/"
    val_xml_path = "./COCO/annotations/val2017/"

    train_txt_path = "./COCO/labels/train2017/"
    val_txt_path = "./COCO/labels/val2017/"

    input_paths = [train_xml_path, val_xml_path]
    output_paths = [train_txt_path, val_txt_path]

    for output_path in output_paths:
        if not os.path.exists(output_path):
            os.mkdir(output_path)
    
    assert len(input_paths) == len(output_paths), 'Error, size of input_paths does not equal to size of output_paths'

    for path_id, path in enumerate(input_paths):
        xml_list = os.listdir(path)
        for xml_id, xml_file in enumerate(xml_list):
            in_file =  open(path + xml_file, 'r')
            out_file = open(output_paths[path_id] + xml_file.split('.')[0] + '.txt', 'a')
            tree=ET.parse(in_file)
            root = tree.getroot()
            size = root.find('size')  
            w = int(size.find('width').text)
            h = int(size.find('height').text)
        
            for obj in root.iter('object'):
                cls = obj.find('name').text
                if cls not in classes_names :
                    continue
                cls_id = classes_names.index(cls)
                xmlbox = obj.find('bndbox')   
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                bb = convert((w,h), b)
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n') 
            print("[{}/{}] Successfully converted from {} to {}".format(xml_id+1, len(xml_list), path + xml_file, output_paths[path_id] + xml_file.split('.')[0] + '.txt'))
            
