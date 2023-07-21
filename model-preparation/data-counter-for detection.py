import os
import glob
import csv

main = 'mypath'                     #path to folder containing splitted datasets
dirs = sorted(os.listdir(main))
print(dirs)

with open(os.path.join(main,'data_total.csv'),'w') as f:
    writer = csv.writer(f)
    writer.writerow(['model','train_bio','train_bul','train_images',
                     'val_bio','val_bul','val_images',
                     'test_bio','test_bul','images'])

    for dir in dirs:
        ## get train and val
        train_bio = 0
        train_bul = 0
        val_bio = 0
        val_bul = 0 
        test_bio = 0
        test_bul = 0
        for type in ['train','val', 'test']:
            #set
            set = type

            #images
            files = glob.glob(os.path.join(main,dir,'data',type,'images/*.jpg'))
            if (type == 'test'):
                files = glob.glob(os.path.join(main,'test/*.jpg'))
            images = len(files)

            #snails_n 
            bio_counter = 0
            bul_counter = 0
            for file in files:
                txt = file.replace('images','labels')
                txt = txt.replace('.jpg','.txt')
                with open(txt, 'r') as text:
                    lines = text.readlines()
                    count = len(lines)

                    if (count > 1):
                        for line in lines:
                            el = line.split()
                            if (el[0] == '0'):
                                bio_counter += 1
                            if (el[0] == '1'):
                                bul_counter += 1
                    if (count == 1):
                        el = lines[0].split(' ')
                        if (el[0] == '0'):
                            bio_counter += 1
                        if (el[0] == '1'):
                            bul_counter += 1
            
            if (type == 'train'):
                train_bio = bio_counter
                train_bul = bul_counter
                train_img = images
            elif (type == 'val'):
                val_bio = bio_counter
                val_bul = bul_counter
                val_img = images
            elif (type == 'test'):
                test_bio = bio_counter
                test_bul = bul_counter
                test_img = images
            
        writer.writerow([dir, train_bio, train_bul,train_img, val_bio, val_bul,val_img,test_bio,test_bul,test_img])