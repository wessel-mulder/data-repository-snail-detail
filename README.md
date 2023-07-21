# data-repository-snail-detail
This repository contains the scripts used in data pre-processing, synthetic-data generation, model-preparation and visualisation of results for my MSc thesis 'Snail detail: Identification of _Schistosoma_ intermediate host snails with synthetic-data trained computer vision networks'.

This folder is divided as per these four 'main' computational steps, along with some example images and data so one can visualise how the scripts work. 
Descriptions of the scripts and data are contained in separate README.md files in every folder. 
The folders are named as follows: 

- pre-processing
This folder contains the script used in removing the backgrounds of images and automatic cropping to image extents

- synthetic-data-generation
This folder contains the script used to generate synthetic data for the base synthetic data pipeline.

- model-preparation
This folder contains multiple scripts and example files for splitting the synthetic data and HQ images into training/validation subsets for both classification and detection. It contains a script to count the number of individuals represented in the synthetic dataset.

- model-testing
This folder contains the script for testing of classification accuracies 

The data used in my project is not shared publicly as it is not mine to share. 




