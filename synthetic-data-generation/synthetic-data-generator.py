### GETTING STARTED ###
import cv2
import os
import numpy as np
import albumentations as A
import time
from tqdm import tqdm
import random
import datetime
from datetime import datetime
import glob

### PARAMETERS
# BG
bg_width = 1080
bg_height = 1920

# Snails
snail_min_nr = 1
snail_max_nr = 20
snail_bright_min = -1
snail_bright_max = 0
snail_contrast_min = 0
snail_contrast_max = 1

### DEFINE PATHS
PATH_TO_FOLDERS = 'my_images_path'          
            # Folder consists of multiple folders for each genus. Each genus-
            # folder contains multiple folders containing all images for one
            # species
PATH_TO_BACKGROUNDS = 'my_backgrounds_path'      
            # Folder consists of all background images to be used
PATH_TO_OUTPUT = 'my_output_path'
            # Folder where output will be generated 

### GET GENERA
obj_dict = {}
genera = sorted(os.listdir(PATH_TO_FOLDERS))
genera = [genus for genus in genera if not genus.startswith('.')]
genera = [genus for genus in genera if genus == 'Bulinus' or genus == 'Biomphalaria']

keys = range(len(genera))
for i in keys:
    obj_dict[i] = {'folder': genera[i], 'longest_min': 150, 'longest_max': 200}

### GET SPECIES & PATHS
for k, _ in obj_dict.items():
    genera = obj_dict[k]['folder']

    species = sorted(os.listdir(os.path.join(PATH_TO_FOLDERS,genera)))
    species = [s for s in species if not s.startswith('.')]

    species_dict = {}
    keys = range(len(species))
    for s in keys:
        binom = species[s]
        species_dict[s] = {'species': binom}

        files_imgs = sorted(os.listdir(os.path.join(PATH_TO_FOLDERS,genera,binom,'cropped')))
        files_imgs = [os.path.join(PATH_TO_FOLDERS,genera,binom,'cropped',f) for f in files_imgs]
    
        species_dict[s]['images'] = files_imgs
    obj_dict[k]['species'] = species_dict

### GET BACKGROUND PATHS
real_bg = sorted(os.listdir(PATH_TO_BACKGROUNDS))
real_bg = [os.path.join(PATH_TO_BACKGROUNDS, f) for f in real_bg if not f.startswith('.')]

### RESIZE TRANSFORM OBJECTS
def resize_transform_obj(img, mask, longest_min, longest_max):

    h, w = mask.shape[0], mask.shape[1]
    
    longest, shortest = max(h, w), min(h, w)
    longest_new = np.random.randint(longest_min, longest_max)
    shortest_new = int(shortest * (longest_new / longest))
    
    if h > w:
        h_new, w_new = longest_new, shortest_new
    else:
        h_new, w_new = shortest_new, longest_new
        
    transform_resize_flip = A.Compose(
        [
            A.Resize(h_new, w_new, interpolation=1, always_apply=True, p=1),
            A.HorizontalFlip(p=0.5),
            A.SafeRotate(limit = 25, border_mode = cv2.BORDER_CONSTANT),
            A.VerticalFlip(p=0.1)
        ]
    )

    transformed_resized = transform_resize_flip(image=img)
    img_t = transformed_resized["image"]
    
    return img_t

### RESIZE IMAGES
def resize_img(img, desired_max, desired_min):

    h, w = img.shape[0], img.shape[1]
    
    longest, shortest = max(h, w), min(h, w)
    longest_new = desired_max
    if desired_min:
        shortest_new = desired_min
    else:
        shortest_new = int(shortest * (longest_new / longest))
    
    if h > w:
        h_new, w_new = longest_new, shortest_new
    else:
        h_new, w_new = shortest_new, longest_new
        
    transform_resize = A.Compose([
        A.Sequential([
        A.Resize(h_new, w_new, interpolation=1, always_apply=False, p=1)
        ], p=1)
    ])
    transformed = transform_resize(image=img)
    img_r = transformed["image"]
        
    return img_r

### TRANSPARENT IMAGE FUNCTION
def add_transparent_image(background,foreground,mask,min_length,max_length,x_coord, y_coord,transforms,label):
    bg_h, bg_w, bg_channels = background.shape
    
    foreground = resize_transform_obj(foreground,mask,min_length,max_length)
    fg_h, fg_w, fg_channels = foreground.shape

    assert bg_channels == 3, f'background image should have exactly 3 channels (RGB). found:{bg_channels}'
    assert fg_channels == 4, f'foreground image should have exactly 4 channels (RGBA). found:{fg_channels}'

    # center by default
    w = min(fg_w, bg_w, fg_w + x_coord, bg_w - x_coord)
    h = min(fg_h, bg_h, fg_h + y_coord, bg_h - y_coord)

    if w < 1 or h < 1: return

    # clip foreground and background images to the overlapping regions
    bg_x = max(0, x_coord)
    bg_y = max(0, y_coord)
    fg_x = max(0, x_coord * -1)
    fg_y = max(0, y_coord * -1)
    foreground = foreground[fg_y:fg_y + h, fg_x:fg_x + w]
    background_subsection = background[bg_y:bg_y + h, bg_x:bg_x + w]

    # separate alpha and color channels from the foreground image
    foreground_colors = foreground[:, :, :3]
    transformed = transforms(image=foreground_colors)
    foreground_colors = transformed['image']

    alpha_channel = foreground[:, :, 3] / 255  # 0-255 => 0.0-1.0

    # construct an alpha_mask that matches the image shape
    alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

    # combine the background with the overlay image weighted by alpha
    composite = background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask

    # overwrite the section of the background image that has been updated
    background[bg_y:bg_y + h, bg_x:bg_x + w] = composite


    xc = (bg_x + (bg_x + w)) / 2
    yc = (bg_y + (bg_y + h)) / 2

    annotations_yolo = [label,
                        round(xc/bg_w, 5),
                        round(yc/bg_h, 5),
                        round(w/bg_w, 5),
                        round(h/bg_h, 5)]
    
    return annotations_yolo

### GET BACKGROUND & COMPOSITION 
def create_bg_with_noise():
    
    idx = np.random.randint(len(real_bg))
    bg_path = real_bg[idx]
    img_bg = cv2.imread(bg_path)
    img_comp_bg = resize_img(img_bg, bg_height, bg_width)

    return img_comp_bg

### DEFINE COORDINATES 
x_es = [180,340,540,740,900]
y_es = [160,360,560,760,960,1160,1360,1560,1760]
total_combinations = len(x_es)*len(y_es)

coord_dict = {}
count = 1
for x in x_es:
    for y in y_es: 
        coord_dict[count] = [x,y]
        count += 1

### PASTING IMAGES AND GENERATING ANNOTATIONS
def create_composition(img_comp_bg):

    r_bright = random.uniform(snail_bright_min,snail_bright_max)
    r_contrast = random.uniform(snail_contrast_min,snail_contrast_max)

    transforms_color = A.Compose(
    [
        A.RandomBrightnessContrast(brightness_limit=(r_bright,r_bright),
                            contrast_limit=(r_contrast,r_contrast),
                            brightness_by_max=True,
                            p=1)] 
        )

    nr = np.random.randint(snail_min_nr, snail_max_nr)
    values = random.sample(range(1, len(coord_dict)),nr)

    bg = img_comp_bg.copy()
    annotations = []

    for value in values:
        x_coord,y_coord = coord_dict[value]
        x_coord = x_coord + random.randint(-50,50)
        y_coord = y_coord + random.randint(-50,50)

        obj_idx = np.random.randint(len(obj_dict)) 
        species_number = len(obj_dict[obj_idx]['species'])
        species_idx = np.random.randint(species_number)

        label = obj_idx
        
        imgs_number = len(obj_dict[obj_idx]['species'][species_idx]['images'])
        idx = np.random.randint(imgs_number)
        img_path = obj_dict[obj_idx]['species'][species_idx]['images'][idx]

        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)

        longest_min = obj_dict[obj_idx]['longest_min']
        longest_max = obj_dict[obj_idx]['longest_max']

        yolo = add_transparent_image(bg,img,mask,longest_min,longest_max,x_coord,y_coord,transforms_color,label)
        annotations.append(yolo)

    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
    return bg,annotations

### GENERATE DATASET FUNCTION
def generate_dataset(imgs_number, folder):
    time_start = time.time()
    for j in tqdm(range(imgs_number)):
        now = datetime.utcnow()
        times = now.strftime('%T:%f')[:-3]
        years = now.strftime('%F')
        mytime = times+'_'+years

        img_comp_bg = create_bg_with_noise()
        img_comp,annotations = create_composition(img_comp_bg)
        
        img_comp = cv2.cvtColor(img_comp, cv2.COLOR_BGR2RGB)
        cv2.imwrite(os.path.join(folder, '{}.jpg').format(mytime), img_comp)

        for i in range(len(annotations)):
            with open(os.path.join(folder, '{}.txt').format(mytime), "a") as f:
                f.write(' '.join(str(el) for el in annotations[i]) + '\n')
                
    time_end = time.time()
    time_total = round(time_end - time_start)
    time_per_img = round((time_end - time_start) / imgs_number, 1)
    
    print("Generation of {} synthetic images is completed. It took {} seconds, or {} seconds per image".format(imgs_number, time_total, time_per_img))

### CHECK IF PATH EXISTS
if not os.path.isdir(os.path.join(PATH_TO_OUTPUT)):
    os.makedirs(os.path.join(PATH_TO_OUTPUT))

### DEFINE NUMBER OF IMAGES TO GENERATED
number = 100
generate = number - len(glob.glob(os.path.join(PATH_TO_OUTPUT)))

### GENERATE
generate_dataset(generate, folder=PATH_TO_OUTPUT)

