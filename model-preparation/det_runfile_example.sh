#!/bin/bash
#Set job requirements

#SBATCH --gpus=1
#SBATCH --partition=gpu
#SBATCH --time=05:00:00
#SBATCH -o _model__%j.out
#SBATCH --mail-type=END
#SBATCH --mail-user=wesselmulder00@gmail.com

cd $HOME/my_ultralytics/_model_/
yolo detect train data=dataset.yaml model=yolov8x.yaml pretrained=yolov8x.pt epochs=300 patience=100 batch=32 imgsz=640 workers=18 project=_model_ 




