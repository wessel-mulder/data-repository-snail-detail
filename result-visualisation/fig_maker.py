import os 
import numpy as np
import cv2

main = '/Volumes/T7/Repos/results_syn_det'

'''
results = ['COLOR','AUGMENT','BACKGROUND','INPUT','POS_NEG','WINDOW']
orders = [['BONE-50','BONE-100','COL-50','COL-100'],
          ['HUE-SAT-BLUR','GAUSSIAN-BLUR','SIZES','SIZE-CONSTANT'],
          ['AUGMENTED','COLORED','ROSES','STAINS','EXTRA-LAYER'],
          ['REAL','REAL-MIX','CYCLEGAN','CYCLEGAN-MIX'],
          ['BOTH-NEG','BRIGHT-NEG','CONTRAST-NEG','BOTH-POS','BRIGHT-POS','CONTRAST-POS'],
          ['WINDOW+-0','WINDOW+-0.1','WINDOW+-0.5','WINDOW+-1']]

letters = ['A.','B.','C.','D.','E.','F.','G.']
for result,my_order in zip(results,orders):
    dir = os.path.join(main,result)
    dirs = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(main,result,d))]
    dirs = [os.path.join(main,result,d) for d in my_order]

    dirs.insert(0,'/Volumes/T7/Repos/results_syn_det/BASE_CS/BASE')
    print(dirs)
    for x1,d in enumerate(dirs):
        print(d)
        source = d
        for x2,y in enumerate([9,70,35,31]):
            if x2 == 0:

                ## load images 
                jpg = str(y)+'.jpg'
                total = cv2.imread(os.path.join(source,'output',jpg))
                h,w,c = total.shape

                ## make border
                total = cv2.copyMakeBorder(src=total, top=100, bottom=10, left=10, right=10, 
                                        borderType=cv2.BORDER_CONSTANT,value = [255,255,255]) 
                
                ## add text 
                els = d.split('/')
                text = letters[x1]+' '+els[-1]

                coordinates = (10,75)                ## x,y
                font = cv2.FONT_HERSHEY_COMPLEX
                fontScale = 2.5
                color = (0,0,0)
                thickness = 3
                total = cv2.putText(total, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)

            else:
                jpg = str(y)+'.jpg'
                img = cv2.imread(os.path.join(source,'output',jpg))
                img = cv2.copyMakeBorder(src=img, top=10, bottom=10, left=10, right=10,
                                         borderType=cv2.BORDER_CONSTANT,value = [255,255,255])
                total = cv2.vconcat([total,img])

        if x1 ==0:
            ## make border
            total = cv2.copyMakeBorder(src=total, top=0, bottom=0, left=100, right=0, 
                                    borderType=cv2.BORDER_CONSTANT,value = [255,255,255]) 
            
            x = 20
            y = 200
            coords = []
            for nr in [0,1,2,3]:
                coords.append((x,int(y+(nr*h)+(nr*20))))
            rows = ['I.','II.','III.','IV.']
            
            for coord,row in zip(coords,rows):
                total = cv2.putText(total, row, coord, font, fontScale, color, thickness, cv2.LINE_AA)   
            total2 = total
        else:
            total2 = cv2.hconcat([total2,total])
    cv2.imwrite(os.path.join(main,'z_comps_hard',result+'_hard.jpg'),total2)

for result,my_order in zip(results,orders):
    dir = os.path.join(main,result)
    dirs = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(main,result,d))]
    dirs = [os.path.join(main,result,d) for d in my_order]

    dirs.insert(0,'/Volumes/T7/Repos/results_syn_det/BASE_CS/BASE')
    print(dirs)
    for x1,d in enumerate(dirs):
        print(d)
        source = d
        for x2,y in enumerate([27,17,52]):
            if x2 == 0:

                ## load images 
                jpg = str(y)+'.jpg'
                total = cv2.imread(os.path.join(source,'output',jpg))
                h,w,c = total.shape

                ## make border
                total = cv2.copyMakeBorder(src=total, top=100, bottom=10, left=10, right=10, 
                                        borderType=cv2.BORDER_CONSTANT,value = [255,255,255]) 
                
                ## add text 
                els = d.split('/')
                text = letters[x1]+' '+els[-1]

                coordinates = (10,75)                ## x,y
                font = cv2.FONT_HERSHEY_COMPLEX
                fontScale = 2.5
                color = (0,0,0)
                thickness = 3
                total = cv2.putText(total, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)

            else:
                jpg = str(y)+'.jpg'
                img = cv2.imread(os.path.join(source,'output',jpg))
                img = cv2.copyMakeBorder(src=img, top=10, bottom=10, left=10, right=10,
                                         borderType=cv2.BORDER_CONSTANT,value = [255,255,255])
                total = cv2.vconcat([total,img])

        if x1 ==0:
            ## make border
            total = cv2.copyMakeBorder(src=total, top=0, bottom=0, left=100, right=0, 
                                    borderType=cv2.BORDER_CONSTANT,value = [255,255,255]) 
            
            x = 20
            y = 200
            coords = []
            for nr in [0,1,2,3,4]:
                coords.append((x,int(y+(nr*h)+(nr*20))))
            rows = ['I.','II.','III.','IV.','V.']
            
            for coord,row in zip(coords,rows):
                total = cv2.putText(total, row, coord, font, fontScale, color, thickness, cv2.LINE_AA)   
            total2 = total
        else:
            total2 = cv2.hconcat([total2,total])
    cv2.imwrite(os.path.join(main,'z_comps_easy',result+'_easy.jpg'),total2)

source = '/Volumes/T7/Repos/results_syn_det/FINAL/'
dirs = [d for d in os.listdir(source) if os.path.isdir(os.path.join(source,d))]
print(dirs)

for d in dirs:
    for x1,y1 in enumerate([9,70,35,31]):
        jpg = str(y1)+'.jpg'
        img = cv2.imread(os.path.join(source,d,'output',jpg))
        h,w,c = img.shape
        img = cv2.copyMakeBorder(src=img, top=10, bottom=10, left=10, right=10,
                                    borderType=cv2.BORDER_CONSTANT,value = [0,0,255])
        img = cv2.copyMakeBorder(src=img, top=90, bottom=0, left=0, right=0,
                                borderType=cv2.BORDER_CONSTANT,value = [255,255,255])
        if x1 == 0:
            top = img
        else:
            top = cv2.hconcat([top,img])

    ## add text 
    xcoord = 10
    ycoord = 75
    coords = []
    for nr in [0,1,2,3]:
        coords.append((int(x1+(nr*w)+(nr*20)),ycoord))
    letters = ['I. DISTANCE',
                'II. BLURRY',
                'III. ROSES',
                'IV. CLUSTERED']

    font = cv2.FONT_HERSHEY_COMPLEX
    fontScale = 2.5
    color = (0,0,0)
    thickness = 3
    for coord,row in zip(coords,letters):
        top = cv2.putText(top, row, coord, font, fontScale, color, thickness, cv2.LINE_AA)

    #### EASY IMAGES
    for x2,y2 in enumerate([27,17,52]):
        jpg = str(y2)+'.jpg'
        img = cv2.imread(os.path.join(source,d,'output',jpg))
        h,w,c = img.shape
        img = cv2.copyMakeBorder(src=img, top=10, bottom=10, left=10, right=10,
                                    borderType=cv2.BORDER_CONSTANT,value = [0,255,0])
        img = cv2.copyMakeBorder(src=img, top=90, bottom=0, left=0, right=0,
                                borderType=cv2.BORDER_CONSTANT,value = [255,255,255])
        if x2 == 0:
            bottom = img
        else:
            bottom = cv2.hconcat([bottom,img])

    example = '/Volumes/T7/Repos/results_syn_det/'+d+'.jpg'
    example = cv2.imread(example)
    example = cv2.resize(example, (w,h))
    crop = cv2.copyMakeBorder(src=example, top=10, bottom=10, left=10, right=10,
                                borderType=cv2.BORDER_CONSTANT,value = [255,0,0])
    crop = cv2.copyMakeBorder(src=crop, top=90, bottom=0, left=0, right=0,
                                borderType=cv2.BORDER_CONSTANT,value = [255,255,255])

    bottom = cv2.hconcat([bottom,crop])


    ## add text 
    xcoord = 10
    ycoord = 75
    coords = []
    for nr in [0,1,2,3]:
        coords.append((int(x2+(nr*w)+(nr*20)),ycoord))
    letters = ['I. BIOMPHALARIA',
                'II. BULINUS',
                'III. BULINUS',
                d]

    font = cv2.FONT_HERSHEY_COMPLEX
    fontScale = 2.5
    color = (0,0,0)
    thickness = 3
    for coord,row in zip(coords,letters):
        bottom = cv2.putText(bottom, row, coord, font, fontScale, color, thickness, cv2.LINE_AA)
    merge = cv2.vconcat([bottom,top])

    cv2.imwrite(os.path.join(main,'z_comps_base',d+'_final_preds.jpg'),merge)
'''
one = cv2.imread('/Volumes/T7/Repos/results_syn_det/z_comps_base/BASE-UPDATE_final_preds.jpg')
two = cv2.imread('/Volumes/T7/Repos/results_syn_det/z_comps_base/CS_final_preds.jpg')

one = cv2.copyMakeBorder(src=one, top=50, bottom=50, left=200, right=50,
                            borderType=cv2.BORDER_CONSTANT,value = [255,255,255])
two = cv2.copyMakeBorder(src=two, top=0, bottom=50, left=200, right=50,
                        borderType=cv2.BORDER_CONSTANT,value = [255,255,255])
merged = cv2.vconcat([one,two])
cv2.imwrite(os.path.join(main,'z_comps_base','merged.jpg'),merged)









