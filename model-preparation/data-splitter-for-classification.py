### this can be repeated with the commented code down below for biomphalaria and bulinus

import os
import shutil
import glob
import random
from random import sample
from tqdm import tqdm
import cv2
import albumentations as A

### transformations: 
snail_bright_min = -0.3
snail_bright_max = 0.3
snail_contrast_min = -0.3
snail_contrast_max = 0.3

transforms_obj = A.Compose([
    A.SafeRotate(limit=45, 
                p = 1,
                mask_value=0,
                border_mode=cv2.BORDER_CONSTANT),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.1),
    A.RandomBrightnessContrast(
    brightness_limit=(snail_bright_min,snail_bright_max),
    contrast_limit=(snail_contrast_min,snail_contrast_max),
    p=1)
    ])

main = 'mypath'                 # path to folder where datasets will be generated
source = 'mypath'               # path to folder containing the original species and their 
                                # respective images

if not os.path.exists(main):
    os.mkdir(main)

### GENERA
### get genera 
dirs = os.listdir(source)

genera = []
for d in dirs:
    elements = d.split('_')
    el = elements[0]
    genera.append(el)
genera = [g for g in genera if not g.startswith('.')]
genera = sorted(list(set(genera)))

### get genera with at least 15 pictures per aspect
dirs_d = []
dirs_v = []
dirs_a = []
dirs = [dirs_d,dirs_v,dirs_a]
wildcards = ['*_d.*','*_v.*','*_a.*']
min_pictures = 15

for g in genera:
    for card,dir in zip(wildcards,dirs):
        nr= glob.glob(os.path.join(source,g+'_*',card))
        if len(nr) > min_pictures:
            dir.append(g)


models = ['gen_d','gen_v','gen_a']
wildcards = ['*_d.*','*_v.*','*_a.*']
list = dirs
modes = ['train','val','test']

test_nr = 5
val = 200
train = 1800

for model,card,dirs in zip(models,wildcards,list):
    if not os.path.exists(os.path.join(main,model)):
        os.mkdir(os.path.join(main,model))

        ## make necessary folders 
        for mode in modes: 
            os.mkdir(os.path.join(main,model,mode))
            for dir in dirs:
                os.mkdir(os.path.join(main,model,mode,dir))

    ## per species 
    for dir in tqdm(dirs):
        
        ## only run incomplete genera 
        test_length = len(os.listdir(os.path.join(main,model,'test',dir)))
        val_length = len(os.listdir(os.path.join(main,model,'val',dir)))
        train_length = len(os.listdir(os.path.join(main,model,'train',dir)))

        if (test_length == test_nr) and (val_length == val) and (train_length == train):
            continue
        else:
            ## get test 
            files = glob.glob(os.path.join(source,dir+'_*',card))
            #files = [file for file in files if not file.endswith('.tif')]
            test = random.sample(range(len(files)),test_nr)
            
            for x,n in enumerate(test):
                jpg = files[n]
                name = str(x)+'.jpg'
                shutil.copy(jpg,
                            os.path.join(main,model,'test',dir,name))

            rest = [x for x in range(len(files)) if not x in test]
        
            ## get val 
            for x in range(val):
                nr = sample(rest,1)[0]
                jpg = files[nr]
                name = str(x)+'.jpg'
                jpg = cv2.imread(jpg)
                transformed = transforms_obj(image=jpg)
                img_t = transformed["image"]
                cv2.imwrite(os.path.join(main,model,'val',dir,name),
                            img_t)
            
            ## get train
            for x in tqdm(range(train),leave = False):
                nr = sample(rest,1)[0]
                jpg = files[nr]
                name = str(x)+'.jpg'
                jpg = cv2.imread(jpg)
                transformed = transforms_obj(image=jpg)
                img_t = transformed["image"]
                cv2.imwrite(os.path.join(main,model,'train',dir,name),
                            img_t)



'''
### BIOMPHALARIA
wildcards = ['*_d.*','*_v.*','*_a.*']
genus = 'Biomphalaria_*'
min_pictures = 15

### get species with at least 15 pictures 
dirs_d = []
dirs_v = []
dirs_a = []
species = glob.glob(os.path.join(source,genus))
for specie in species:
        D = glob.glob(os.path.join(specie,wildcards[0]))
        if len(D) > min_pictures:
            name = os.path.basename(specie)
            dirs_d.append(name)


        V = glob.glob(os.path.join(specie,wildcards[1]))
        if len(V) > min_pictures:
            name = os.path.basename(specie)
            dirs_v.append(name)

        An = glob.glob(os.path.join(specie,wildcards[2]))
        if len(An) > min_pictures:
            name = os.path.basename(specie)
            dirs_a.append(name)
        print(specie,len(D),len(V),len(An))

print(dirs_d)
print(dirs_v)
print(dirs_a)
list = [dirs_d,dirs_v,dirs_a]
models = ['bio_d','bio_v','bio_a']
wildcards = ['*_d.*','*_v.*','*_a.*']
modes = ['train','val','test']
test_nr = 5
val = 200
train = 1800

for model,card,dirs in zip(models,wildcards,list):
    if not os.path.exists(os.path.join(main,model)):
        os.mkdir(os.path.join(main,model))

        ## make necessary folders 
        for mode in modes: 
            os.mkdir(os.path.join(main,model,mode))
            for dir in dirs:
                os.mkdir(os.path.join(main,model,mode,dir))

    ## per species 
    for dir in tqdm(dirs):
        
        ## only run incomplete genera 
        test_length = len(os.listdir(os.path.join(main,model,'test',dir)))
        val_length = len(os.listdir(os.path.join(main,model,'val',dir)))
        train_length = len(os.listdir(os.path.join(main,model,'train',dir)))

        if (test_length == test_nr) and (val_length == val) and (train_length == train):
            continue
        else:
            ## get test 
            files = glob.glob(os.path.join(source,dir,card))
            #files = [file for file in files if not file.endswith('.tif')]
            test = random.sample(range(len(files)),test_nr)
            
            for x,n in enumerate(test):
                jpg = files[n]
                name = str(x)+'.jpg'
                shutil.copy(jpg,
                            os.path.join(main,model,'test',dir,name))

            rest = [x for x in range(len(files)) if not x in test]
        
            ## get val 
            for x in range(val):
                nr = sample(rest,1)[0]
                jpg = files[nr]
                name = str(x)+'.jpg'
                jpg = cv2.imread(jpg)
                transformed = transforms_obj(image=jpg)
                img_t = transformed["image"]
                cv2.imwrite(os.path.join(main,model,'val',dir,name),
                            img_t)
            
            ## get train
            for x in tqdm(range(train)):
                nr = sample(rest,1)[0]
                jpg = files[nr]
                name = str(x)+'.jpg'
                jpg = cv2.imread(jpg)
                transformed = transforms_obj(image=jpg)
                img_t = transformed["image"]
                cv2.imwrite(os.path.join(main,model,'train',dir,name),
                            img_t)
'''
'''
#### BULINUS
wildcards = ['*_d.*','*_v.*']
genus = 'Bulinus_*'


min_pictures = 15

### get species with at least 15 pictures 
dirs = []
species = glob.glob(os.path.join(source,genus))
for specie in species:
        D = glob.glob(os.path.join(specie,wildcards[0]))
        #D = [jpg for jpg in D if not jpg.endswith('.tif')]


        V = glob.glob(os.path.join(specie,wildcards[1]))
        #V = [jpg for jpg in V if not jpg.endswith('.tif')]

        if len(D) > min_pictures and len(V) > min_pictures:
            name = os.path.basename(specie)
            dirs.append(name)

models = ['bul_d','bul_v']
wildcards = ['*_d.*','*_v.*']
modes = ['train','val','test']
test_nr = 5
val = 200
train = 1800

for model,card in zip(models,wildcards):
    if not os.path.exists(os.path.join(main,model)):
        os.mkdir(os.path.join(main,model))

        ## make necessary folders 
        for mode in modes: 
            os.mkdir(os.path.join(main,model,mode))
            for dir in dirs:
                os.mkdir(os.path.join(main,model,mode,dir))

    ## per species 
    for dir in tqdm(dirs):
        
        ## only run incomplete genera 
        test_length = len(os.listdir(os.path.join(main,model,'test',dir)))
        val_length = len(os.listdir(os.path.join(main,model,'val',dir)))
        train_length = len(os.listdir(os.path.join(main,model,'train',dir)))

        if (test_length == test_nr) and (val_length == val) and (train_length == train):
            continue
        else:
            ## get test 
            files = glob.glob(os.path.join(source,dir,card))
            #files = [file for file in files if not file.endswith('.tif')]
            test = random.sample(range(len(files)),test_nr)
            
            for n in test:
                jpg = files[n]
                name = os.path.basename(jpg)
                shutil.copy(jpg,
                            os.path.join(main,model,'test',dir,name))

            rest = [x for x in range(len(files)) if not x in test]
        
            ## get val 
            for x in range(val):
                nr = sample(rest,1)[0]
                jpg = files[nr]
                name = str(x)+'.jpg'
                jpg = cv2.imread(jpg)
                transformed = transforms_obj(image=jpg)
                img_t = transformed["image"]
                cv2.imwrite(os.path.join(main,model,'val',dir,name),
                            img_t)
            
            ## get train
            for x in range(train):
                nr = sample(rest,1)[0]
                jpg = files[nr]
                name = str(x)+'.jpg'
                jpg = cv2.imread(jpg)
                transformed = transforms_obj(image=jpg)
                img_t = transformed["image"]
                cv2.imwrite(os.path.join(main,model,'train',dir,name),
                            img_t)

                            
'''              






    
