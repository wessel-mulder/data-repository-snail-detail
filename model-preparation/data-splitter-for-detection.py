import glob
import random
import os
import shutil
from tqdm import tqdm

main = 'mypath'             # path to folder were datasets will be moved to 
og = 'mypath'               # path to folder containing original synthetic datasets
                            # each in their respective folder
names = os.listdir(og)
 
paths = [os.path.join(og,f) for f in names]
print(paths)
print(names)

### split
modes = ['train','val']
types = ['images','labels']
train_nr = 1800
val_nr = 200

for model,path2syn in tqdm(zip(names,paths)):
    if not os.path.exists(os.path.join(main,model)):
        os.mkdir(os.path.join(main,model))
        os.mkdir(os.path.join(main,model,'data'))
        
        for mode in modes:
            os.mkdir(os.path.join(main,model,'data',mode))
            for type in types:
                os.mkdir(os.path.join(main,model,'data',mode,type))

        ### GRAB files
        files = glob.glob(os.path.join(path2syn,'*.jpg'))

        train = random.sample(range(len(files)),train_nr)
        rest = [x for x in range(len(files)) if not x in train]
        val= random.sample(rest,val_nr)

        for y,set in enumerate([train,val]):
            for n in set:
                jpg_source = files[n]
                txt_source = jpg_source.replace('.jpg','.txt')

                jpg = os.path.basename(jpg_source)
                txt = jpg.replace('.jpg','.txt')
                shutil.copy(jpg_source,
                            os.path.join(main,model,'data',modes[y],'images',jpg))
                shutil.copy(txt_source,
                            os.path.join(main,model,'data',modes[y],'labels',txt))

