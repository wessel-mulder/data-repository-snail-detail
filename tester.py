
from ultralytics import YOLO
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import torch
import torchmetrics
from torchmetrics.classification import MulticlassAveragePrecision,MulticlassConfusionMatrix,MulticlassAccuracy,MulticlassAUROC,MulticlassPrecision,MulticlassRecall
import cv2
from sklearn import preprocessing
import glob
import os 
from numpy import asarray
import csv

models = ['gen_a','gen_d','gen_v']

with open('GEN_CLS_accuracies.csv','w') as f: 
    f_writer = csv.writer(f)
    f_writer.writerow(['model','species','species_count','averageprecision','accuracy','auroc','precision','recall'])
    for model in models:
        with open(model+'_confusion_matrix.csv','w') as g:
            g_writer = csv.writer(g)
            with open(model+'_gg_matrix.csv','w') as h:
                h_writer = csv.writer(h)
                
                model_source = '/Volumes/T7/Repos/results_HQ_cls/'+model+'/best.pt'
                yolo = YOLO(model_source)

                test_path = '/Volumes/T7/Repos/splitter/HQ_cls/'+model+'/test/'
                dirs = sorted(os.listdir(test_path))

                counts = []
                for s in dirs:
                    path = '/Volumes/T7/Repos/z_old/bg_remover/DATA/'+s+'_*'
                    if (model == 'gen_d'):
                        files = glob.glob(os.path.join(path,'*_d.*',))
                        length = len(files)
                        counts.append(length)
                    if (model == 'gen_v'):
                        files = glob.glob(os.path.join(path,'*_v.*',))
                        length = len(files)
                        counts.append(length)
                    if (model == 'gen_a'):
                        files = glob.glob(os.path.join(path,'*_a.*',))
                        length = len(files)
                        counts.append(length)
                
                class_nr = len(os.listdir('/Volumes/T7/Repos/splitter/HQ_cls/'+model+'/test/'))
                nrs = []
                for x in range(class_nr):
                    for _ in range(5):
                        nrs.append(x)
                target = torch.tensor(nrs)

                output = []
                for x,dir in enumerate(dirs):

                    imgs = (os.path.join(test_path,dir))
                    res = yolo(imgs)
                    preds = torch.empty(5, class_nr)

                    for y,r in enumerate(res):
                        probs = r.probs
                        preds[y] = probs

                    for one in preds:
                        output.append(one)

                preds = torch.vstack(output)

                average_precision = MulticlassAveragePrecision(num_classes=class_nr, average=None)
                av_p = average_precision(preds, target)

                accuracy = MulticlassAccuracy(num_classes = class_nr,average = None)
                acc = accuracy(preds,target)

                auroc = MulticlassAUROC(num_classes = class_nr,average=None)
                auc = auroc(preds,target)

                recall = MulticlassRecall(num_classes = class_nr,average=None)
                rec = recall(preds,target)  

                precision = MulticlassPrecision(num_classes = class_nr,average=None)
                prec = precision(preds,target)              

                for dir,count,av,ac,au,re,pr in zip(dirs,counts,av_p,acc,auc,rec,prec):
                    f_writer.writerow([model,dir,count,av.item(),ac.item(),au.item(),re.item(),pr.item()])
                
                first_row = ['species']
                for s in dirs:
                    first_row.append(s)
                g_writer.writerow(first_row)

                matrix = MulticlassConfusionMatrix(num_classes=class_nr)
                cm = matrix(preds,target)
                for dir,row in zip(dirs,cm):
                    write = row.tolist()
                    write.insert(0,dir)
                    g_writer.writerow(write)
                
                h_writer.writerow(['predict','target','n'])
                for dir,row in zip(dirs,cm):
                    write = row.tolist()
                    for dir2,col in zip(dirs,write):
                        h_writer.writerow([dir,dir2,col])

                


            





