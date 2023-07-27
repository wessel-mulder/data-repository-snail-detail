# This folder contains multiple scripts for splitting the data into training/validation subsets for classification and detection

For the **detection tasks**, the following scripts were used:

_data-splitter-for-detection.py_ was used to split the synthetic-images into a training and a validation subset.

_yaml-writer-detection.py_ was used to write the .yaml files for each individual model. These files contain the paths to the folders containing the training and validation images, the number of classes and class names. These are used to update the last layer of the pretrained model.

_runfile-writer-detection.py_ was used to generate .sh runfiles for each individual model, based on the template _runfile-example-detection.sh_. 

_data-counter-for-detection.py_ was used to count the number of individuals represented for each class and the total number of images used, across both training, validation and testing images for each model.

For the **classification tasks**, the following scripts were used:

_data-splitter-for-classification.py_ was used to upsample the high-quality images into a training and a validation subset through image augmentation.

_runfile-writer-classification.py_ was used to generate .sh runfiles for each individual model, based on the template _runfile-example-classification.sh_. 




