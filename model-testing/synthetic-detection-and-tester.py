### interpreter op 3.10

from ultralytics import YOLO
import cv2
import torch
from torchmetrics.detection.mean_ap import MeanAveragePrecision
import cv2
import glob
import os 
import csv
from tqdm import tqdm 

##get targets
main_dir = 'mypath'         # directory contain folders each named after model name. these model-folders
                            # contain a folder called 'train', which contains a folder named 'weights', 
                            # in which the best model weights are stored as 'best.pt'
test = 'mypath'             # directory containing all the test images

files = glob.glob(os.path.join(test,'*.jpg'))
target = []
for file in files:
    jpg = file
    txt = file.replace('.jpg','.txt')
    img = cv2.imread(jpg)
    w, h = img.shape[1], img.shape[0]
    txt = file.replace('.jpg','.txt')

    with open(txt) as f:
        lines = f.readlines()
        n = len(lines)
        all_cls = []
        all_boxes = []
        for line in lines:
            elements = line.split(' ')
            all_cls.append(int(elements[0]))
            coords = [
                round(float(elements[1])*w,5),
                round(float(elements[2])*h,5),
                round(float(elements[3])*w,5),
                round(float(elements[4])*h,5)
            ]
            all_boxes.append(coords)

    this_dict = dict(
            boxes=torch.tensor(all_boxes, device = torch.device('cpu',0)),
            labels=torch.tensor(all_cls, device = torch.device('cpu',0))
    )
    target.append(this_dict)

dirs = os.listdir(main_dir)
dirs = [dir for dir in dirs if not dir.__contains__('.')]

with open('models_best_update.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(['model','stat','value'])

    for dir in dirs:
        print(dir)
        best = YOLO(os.path.join(main_dir,dir,'train/weights/best.pt'))

        ## create lists for storing dictionaries
        ### one dictionary is one image 
        preds = []
        results = best(files,stream = True,conf=0.5)

        for res in results:
            res_boxes = res.boxes.xywh
            res_cls = res.boxes.cls
            #res_cls = list(map(lambda nr: int(nr),res_cls))        
            res_conf = res.boxes.conf
            that_dict = dict(
                boxes=torch.tensor(res_boxes, device = torch.device('cpu',0)),
                scores=torch.tensor(res_conf, device = torch.device('cpu',0)),
                labels=torch.tensor(res_cls, device = torch.device('cpu',0)),
            )
            preds.append(that_dict)

        metric = MeanAveragePrecision(box_format='cxcywh',iou_type='bbox',iou_thresholds=[0.5],class_metrics=True).to(torch.device('cpu',0))
        metric.update(preds,target)
        my_dict = metric.compute()
        mod = dir 
        stats = list(my_dict.keys())

        for key in stats:
            if key == 'map_per_class':
                map_bio = my_dict[key][0].detach().numpy()
                map_bul = my_dict[key][1].detach().numpy()
                writer.writerow([mod,'map_bio',map_bio])
                writer.writerow([mod,'map_bul',map_bul])  

            elif key == 'mar_100_per_class':
                mar_bio = my_dict[key][0].detach().numpy()
                mar_bul = my_dict[key][1].detach().numpy()
                writer.writerow([mod,'mar_100_bio',mar_bio])
                writer.writerow([mod,'mar_100_bul',mar_bul])  

            else:
                writer.writerow([mod,key,my_dict[key].detach().numpy()])

        if not os.path.exists(os.path.join(main_dir,dir,'output')):
            os.mkdir(os.path.join(main_dir,dir,'output'))

            results = best(files,stream = True,conf=0.5)

            for x,r in enumerate(results):
                result = r.plot(show_conf = False, line_width = 1, font_size = 1)
                cv2.imwrite(os.path.join(main_dir,dir,'output',str(x)+'.jpg'),result)
