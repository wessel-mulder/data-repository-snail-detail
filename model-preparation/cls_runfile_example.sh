#!/bin/bash
#Set job requirements

#SBATCH --gpus=1
#SBATCH --partition=gpu
#SBATCH --time=08:00:00
#SBATCH -o _model__%j.out
#SBATCH --mail-type=END
#SBATCH --mail-user=wesselmulder00@gmail.com

yolo classify train data=_model_ model=yolov8x-cls.yaml pretrained=yolov8x-cls.pt epochs=300 patience=100 batch=32 imgsz=640 workers=18 project=_model_ 




