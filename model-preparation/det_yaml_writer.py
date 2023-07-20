import shutil
import os 
import sys

main = 'splitter/models_sense2'
dirs = [d for d in os.listdir(main) if os.path.isdir(os.path.join(main, d))]

for model in dirs:
    if not model == 'test':
        path = os.path.join(main,model)
        with open(os.path.join(path,'dataset.yaml'),'w') as f:
            f.write("path: '/home/wmulder/my_ultralytics/"+model+"' \n")
            f.write("train: 'data/train/images/' \n")
            f.write("val: 'data/val/images/' \n")
            f.write("\n")
            f.write("nc: 2 \n")
            f.write("names: [Biomphalaria, Bulinus]")

