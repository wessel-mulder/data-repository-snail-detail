import os
import os.path 
from pathlib import Path
from rembg import remove, new_session
import glob
from tqdm import tqdm
import shutil
import cv2 
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np 


PATH_MAIN = 'z_old/bg_remover/samples'
myfolders = sorted(os.listdir(PATH_MAIN))

mypaths = [os.path.join(PATH_MAIN, m) for m in myfolders if not m.startswith('.')]

session = new_session()

count = 0
for p in mypaths:
    count += len(os.listdir(p))
'''
pbar = tqdm(total = count)

for path in mypaths:
    my_dir = os.path.join(path,'rembg')
    image_path = os.path.join(path,'original')


    for thing in [my_dir, image_path]:
        if os.path.exists(thing):
            pass
        else:
            os.makedirs(thing)

        
    for file in Path(path).glob('*.jpg'):
        input_path = str(file)
        file = Path(file)
        output_path = str(file.parent / 'rembg' / (file.stem + ".out.jpg"))

        with open(input_path, 'rb') as i:
            with open(output_path, 'wb') as o:
                input = i.read()
                output = remove(input, session=session)
                o.write(output)
                pbar.update(1)

pbar.close()
'''
if not os.path.exists('/Volumes/T7/Repos/z_old/bg_remover/samples/BIOs/cropped'):
    os.mkdir('/Volumes/T7/Repos/z_old/bg_remover/samples/BIOs/cropped')

if not os.path.exists('/Volumes/T7/Repos/z_old/bg_remover/samples/BULs/cropped'):
    os.mkdir('/Volumes/T7/Repos/z_old/bg_remover/samples/BULs/cropped')

for dir in ['BIOs','BULs']:
    path = '/Volumes/T7/Repos/z_old/bg_remover/samples/'+dir+'/rembg/'
    output = '/Volumes/T7/Repos/z_old/bg_remover/samples/'+dir
    imgs = glob.glob(path+'*.jpg')
    for img_path in imgs:
        name = os.path.basename(img_path)[:-4]
        print(name)
        img = Image.open(img_path)
        img2 = img.crop(img.getbbox())
        img2.save(output+'/cropped/'+name+'.png')

