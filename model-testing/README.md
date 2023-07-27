# This folder contains the script for testing of prediction accuracies

The Python file _hq-classification-and-tester.py_ was used to generate the **accuracies of model predictions** in classifying high-quality snail images. 

The script generates three CSV files; the first describes different accuracy metrics achieved by a certain model for each individual class. It also counts the number of original source images used to train the model. The second CSV file generates a confusion matrix, where the first column describes the predicted classes and the first row describes the ground truth classes. The third CSV file melts the previous CSV into three columns; a prediction, ground truth and counter column. This file summarizes the confusion matrix in a more workable format.
