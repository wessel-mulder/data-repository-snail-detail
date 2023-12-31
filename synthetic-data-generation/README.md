# This folder contains the script used to generate synthetic data

The Python script _synthetic-data-generator.py_ was used to **generate synthetic images** from the backgroundless, cropped high-quality snails created in pre-processing. 
  
First, a set of parameters are defined, like the sizes of the background and the values used in the compositing of synthetic images and image augmentation. In each iteration, one synthetic images generated. Multiple snails can be pasted on top of the background to create the composite image. Backgrounds are resized to a constant size, while snails are subject to heavier photometric and geometric adjustments. A transparent image function is used to overlay the 'transparent' pixels of the png-snails over the background. In each pasting of the snail, an annotation label is made that describe the coordinates of the bounding boxes of the snails. The YOLO-format is used [x_center, y_center, width, height]. This script will generate however many images the user wants to create, with object annotations in a .txt file of the same name. The synthetic images are named based on the date and time, so users can easily manipulate batches created on certain days and no image will get the same name twice. 
  
  
