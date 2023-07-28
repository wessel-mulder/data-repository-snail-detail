library(ggplot2)
library(ggpubr)
library(cowplot)
library(jpeg)
library(patchwork)
library(magick)
library(ggimage)

setwd('~/Desktop/')
data_total = rbind(read.csv('results_0905/models_best_update.csv'),
                   read.csv('results_0805/models_best_update.csv'),
                   read.csv('results_1505/models_best_update.csv'),
                   read.csv('results_1605/models_best_update.csv'),
                   read.csv('results_2505/models_best_update.csv'),
                   read.csv('results_3005/models_best_update.csv'))
setwd('~/Desktop/get_syn_graphs/')
unique(data_total$model)

### BASE 
og = c('NONE','CS','UPDATED')
new = c('BASE','CS','BASE-UPDATE')
group = 'final'
len = length(og)
for (x in 1:len){
  data_total$group[data_total$model == og[x]] <- group
  data_total$model[data_total$model == og[x]] <- new[x]
}

og = c('HUESATBLUR','BLUR_GAUSS','SIZE','SIZECONSTANT')
new = c('HUE-SAT-BLUR','GAUSSIAN-BLUR','SIZES','SIZE-CONSTANT')
group = 'augmentations'
len = length(og)
for (x in 1:len){
  data_total$group[data_total$model == og[x]] <- group
  data_total$model[data_total$model == og[x]] <- new[x]
}

og = c('REAL','HQ_CS_MIX','cycleGAN','HQ_CG_MIX')
new = c('REAL','BASE-REAL-MIX','CYCLEGAN','BASE-CYCLEGAN-MIX')
group = 'input'
len = length(og)
for (x in 1:len){
  data_total$group[data_total$model == og[x]] <- group
  data_total$model[data_total$model == og[x]] <- new[x]
}

og = c('BG_COL','BG_AUGMENT','EXTRA_LAYER','STAINS','ROSES')
new = c('COLORED','AUGMENTED','EXTRA-LAYER','STAINS','ROSES')
group = 'background'
len = length(og)
for (x in 1:len){
  data_total$group[data_total$model == og[x]] <- group
  data_total$model[data_total$model == og[x]] <- new[x]
}

og = c('bothneg','bothpos','CONTRAST_NEG','BRIGHT_NEG','CONTRAST_POS','BRIGHT_POS')
new = c('BOTH-NEG','BOTH-POS','CONTRAST-NEG','BRIGHT-NEG','CONTRAST-POS','BRIGHT-POS')
group = 'positive-negative'
len = length(og)
for (x in 1:len){
  data_total$group[data_total$model == og[x]] <- group
  data_total$model[data_total$model == og[x]] <- new[x]
}

og = c('BOTH_ZERO','BOTH_MAX','WINDOWSMALL','WINDOW')
new = c('WINDOW±0','WINDOW±1','WINDOW±0.1','WINDOW±0.5')
group = 'window'
len = length(og)
for (x in 1:len){
  data_total$group[data_total$model == og[x]] <- group
  data_total$model[data_total$model == og[x]] <- new[x]
}
write.csv(data_total,'data_total.csv')


# coords ------------------------------------------------------------------


bottom = 0.07
top = 0.33
add = 0.05
n = 1

coords = list()
for (x in 3:7){
  sub_coords = list()
  temp = x -1
  for (y in 0:temp){
    left = (n/x)/2+(y*(n/x)) - add
    right = (n/x)/2+(y*(n/x)) + add
    middle = (n/x)/2+(y*(n/x)) 
    num = y + 1
    sub_coords[[num]] = list(c(bottom,top,left,right,middle))
    print(middle)
  }
  coords[[x]] = sub_coords
}

# mAP, BIO and BULS across models first try -----------------------------------------------------------
stats =  c('map','map_bio','map_bul')
new_data <- subset(data_total, stat %in% stats)

names = c('FINAL', 'AUGMENTATIONS','BACKGROUND','INPUT','POS_NEG','WINDOW')
final = c('BASE', 'BASE-UPDATE','CS')
augmentation = c('BASE','HUE-SAT-BLUR','GAUSSIAN-BLUR','SIZES','SIZE-CONSTANT')
background = c('BASE','AUGMENTED','COLORED','ROSES','STAINS','EXTRA-LAYER')
input = c('BASE','REAL','BASE-REAL-MIX','CYCLEGAN','BASE-CYCLEGAN-MIX')
brightcol = c('BASE','BOTH-NEG','BRIGHT-NEG','CONTRAST-NEG','BOTH-POS','BRIGHT-POS','CONTRAST-POS')
window = c('BASE','WINDOW±0','WINDOW±0.1','WINDOW±0.5','WINDOW±1')
model_list = list(final,augmentation,background,input,brightcol,window)

for (it in seq_along(names)){
  models = model_list[[it]]
  new_new <- subset(new_data, model %in% models)
  new_new$model = factor(new_new$model,levels = models)
  
  all <- ggplot(new_new, aes(x = model, y = value, shape = stat)) +
    geom_point() +
    scale_shape_manual(values = c(1,3,4),
                       name = 'Statistic',
                       labels = c('mAP50','AP50 Biomphalaria','AP50 Bulinus')) +
    #theme_minimal() + 
    scale_y_continuous(name = 'Value',
                       limits = c(0,1))+
    scale_x_discrete(name = 'Model')+
    theme(legend.position = 'top',
          legend.direction = 'horizontal') 
  print(all)
  #Combine plot & images
  length = length(models)
  copy <- all
  
  #x = length*2+1
  #for (mod in 1:length){
  #  name <- models[mod]
  #  jpg_name <- paste0(name,'.jpg')
  #  pic <- readJPEG(jpg_name,native = T)
    #these_coords <- coords[[length]]
    #exact_coords <- these_coords[[mod]]
    #print(exact_coords)
  
  #  copy <- copy +
  #    inset_element(p = pic,
  #                bottom = 0.0,top = 0.3,
  #                  left = (x - 0.25),right = (x+0.25))
   # }
  
  name = paste0(names[it],'.pdf')
  print(name)
  pdf(file = name,
      width = 8,
      height = 8)
  print(copy)
  dev.off()
}






# second try --------------------------------------------------------------

stats =  c('map','map_bio','map_bul')
new_data <- subset(data_total, stat %in% stats)

names = c('FINAL', 'AUGMENTATIONS','BACKGROUND','INPUT','POS_NEG','WINDOW')
final = c('BASE', 'BASE-UPDATE','CS')
augmentation = c('BASE','HUE-SAT-BLUR','GAUSSIAN-BLUR','SIZES','SIZE-CONSTANT')
background = c('BASE','AUGMENTED','COLORED','ROSES','STAINS','EXTRA-LAYER')
input = c('BASE','REAL','BASE-REAL-MIX','CYCLEGAN','BASE-CYCLEGAN-MIX')
brightcol = c('BASE','BOTH-NEG','BRIGHT-NEG','CONTRAST-NEG','BOTH-POS','BRIGHT-POS','CONTRAST-POS')
window = c('BASE','WINDOW±0','WINDOW±0.1','WINDOW±0.5','WINDOW±1')
model_list = list(final,augmentation,background,input,brightcol,window)


# final -------------------------------------------------------------------

new_new <- subset(new_data, model %in% final)
new_new$model = factor(new_new$model,levels = final)

graph <- ggplot(new_new, aes(x = model, y = value, shape = stat)) +
  geom_point() +
  scale_shape_manual(values = c(1,3,4),
                     name = 'Statistic',
                     labels = c('mAP50','AP50 Biomphalaria','AP50 Bulinus')) +
  scale_y_continuous(name = 'Value',
                     limits = c(0,1))+
  theme_minimal() +
  scale_x_discrete(name = 'Model')+
  theme(legend.position = 'top',
        legend.direction = 'horizontal') 

number = length(final)

coord = 0.5
pimage <- axis_canvas(graph, axis = 'x') 
for (i in 1:number){
  print(final[i])
  print(i)
  pimage <- pimage +
    draw_image(paste0(final[i],'.jpg'), x = coord) 
  coord = coord + 1
  print(paste0(final[i],'.jpg'))
}


pimage <- axis_canvas(graph, axis = 'x') +
  draw_image('BASE.jpg', x = 0.5) +
  draw_image('BASE-UPDATE.jpg', x = 1.5) +
  draw_image('CS.jpg', x = 2.5) 

composite <- ggdraw(insert_xaxis_grob(graph, 
                         pimage, 
                         position = 'bottom',
                         height  = grid::unit(1, 'null')))

pdf(file = 'FINAL.pdf',
    width = 8,
    height = 8)
print(composite)
dev.off()



# posneg ------------------------------------------------------------------

new_new <- subset(new_data, model %in% brightcol)
new_new$model = factor(new_new$model,levels = brightcol)

graph <- ggplot(new_new, aes(x = model, y = value, shape = stat)) +
  geom_point() +
  scale_shape_manual(values = c(1,3,4),
                     name = 'Statistic',
                     labels = c('mAP50','AP50 Biomphalaria','AP50 Bulinus')) +
  scale_y_continuous(name = 'Value',
                     limits = c(0,1))+
  theme_minimal() +
  scale_x_discrete(name = 'Model')+
  theme(legend.position = 'top',
        legend.direction = 'horizontal') 

pimage <- axis_canvas(graph, axis = 'x') +
  draw_image('BASE.jpg', x = 0.5) +
  draw_image('BOTH-NEG.jpg', x = 1.5) +
  draw_image('BRIGHT-NEG.jpg', x = 2.5) +
  draw_image('CONTRAST-NEG.jpg', x = 3.5) +
  draw_image('BOTH-POS.jpg', x = 4.5) +
  draw_image('BRIGHT-POS.jpg', x = 5.5) +
  draw_image('CONTRAST-POS.jpg', x = 6.5) 

composite <- ggdraw(insert_xaxis_grob(graph, 
                                      pimage, 
                                      position = 'bottom',
                                      height  = grid::unit(0.3, 'null')))

pdf(file = 'POSNEG.pdf',
    width = 8,
    height = 8)
print(composite)
dev.off()




# AUGMENT ------------------------------------------------------------------

new_new <- subset(new_data, model %in% augmentation)
new_new$model = factor(new_new$model,levels = augmentation)

graph <- ggplot(new_new, aes(x = model, y = value, shape = stat)) +
  geom_point() +
  scale_shape_manual(values = c(1,3,4),
                     name = 'Statistic',
                     labels = c('mAP50','AP50 Biomphalaria','AP50 Bulinus')) +
  scale_y_continuous(name = 'Value',
                     limits = c(0,1))+
  theme_minimal() +
  scale_x_discrete(name = 'Model')+
  theme(legend.position = 'top',
        legend.direction = 'horizontal') 

pimage <- axis_canvas(graph, axis = 'x') +
  draw_image('BASE.jpg', x = 0.5) +
  draw_image('HUE-SAT-BLUR.jpg', x = 1.5) +
  draw_image('GAUSSIAN-BLUR.jpg', x = 2.5) +
  draw_image('SIZES.jpg', x = 3.5) +
  draw_image('SIZE-CONSTANT.jpg', x = 4.5) 

composite <- ggdraw(insert_xaxis_grob(graph, 
                                      pimage, 
                                      position = 'bottom',
                                      height  = grid::unit(0.5, 'null')))

pdf(file = 'AUGMENTATIONS.pdf',
    width = 8,
    height = 8)
print(composite)
dev.off()




# BG ------------------------------------------------------------------

new_new <- subset(new_data, model %in% background)
new_new$model = factor(new_new$model,levels = background)

graph <- ggplot(new_new, aes(x = model, y = value, shape = stat)) +
  geom_point() +
  scale_shape_manual(values = c(1,3,4),
                     name = 'Statistic',
                     labels = c('mAP50','AP50 Biomphalaria','AP50 Bulinus')) +
  scale_y_continuous(name = 'Value',
                     limits = c(0,1))+
  theme_minimal() +
  scale_x_discrete(name = 'Model')+
  theme(legend.position = 'top',
        legend.direction = 'horizontal') 

pimage <- axis_canvas(graph, axis = 'x') +
  draw_image('BASE.jpg', x = 0.5) +
  draw_image('AUGMENTED.jpg', x = 1.5) +
  draw_image('COLORED.jpg', x = 2.5) +
  draw_image('ROSES.jpg', x = 3.5) +
  draw_image('STAINS.jpg', x = 4.5) +
  draw_image('EXTRA-LAYER.jpg', x = 5.5) 

composite <- ggdraw(insert_xaxis_grob(graph, 
                                      pimage, 
                                      position = 'bottom',
                                      height  = grid::unit(0.4, 'null')))

pdf(file = 'BACKGROUND.pdf',
    width = 8,
    height = 8)
print(composite)
dev.off()


# window ------------------------------------------------------------------

new_new <- subset(new_data, model %in% window)
new_new$model = factor(new_new$model,levels = window)

graph <- ggplot(new_new, aes(x = model, y = value, shape = stat)) +
  geom_point() +
  scale_shape_manual(values = c(1,3,4),
                     name = 'Statistic',
                     labels = c('mAP50','AP50 Biomphalaria','AP50 Bulinus')) +
  scale_y_continuous(name = 'Value',
                     limits = c(0,1))+
  theme_minimal() +
  scale_x_discrete(name = 'Model')+
  theme(legend.position = 'top',
        legend.direction = 'horizontal') 

pimage <- axis_canvas(graph, axis = 'x') +
  draw_image('BASE.jpg', x = 0.5) +
  draw_image('WINDOW±0.jpg', x = 1.5) +
  draw_image('WINDOW±0.1.jpg', x = 2.5) +
  draw_image('WINDOW±0.5.jpg', x = 3.5) +
  draw_image('WINDOW±1.jpg', x = 4.5) 

composite <- ggdraw(insert_xaxis_grob(graph, 
                                      pimage, 
                                      position = 'bottom',
                                      height  = grid::unit(0.5, 'null')))

pdf(file = 'WINDOW.pdf',
    width = 8,
    height = 8)
print(composite)
dev.off()






# INPUT ------------------------------------------------------------------

new_new <- subset(new_data, model %in% input)
new_new$model = factor(new_new$model,levels = input)

graph <- ggplot(new_new, aes(x = model, y = value, shape = stat)) +
  geom_point() +
  scale_shape_manual(values = c(1,3,4),
                     name = 'Statistic',
                     labels = c('mAP50','AP50 Biomphalaria','AP50 Bulinus')) +
  scale_y_continuous(name = 'Value',
                     limits = c(0,1))+
  theme_minimal() +
  scale_x_discrete(name = 'Model')+
  theme(legend.position = 'top',
        legend.direction = 'horizontal') 

pimage <- axis_canvas(graph, axis = 'x') +
  draw_image('BASE.jpg', x = 0.5) +
  draw_image('REAL.jpg', x = 1.5) +
  draw_image('BASE-REAL-MIX.jpg', x = 2.5) +
  draw_image('CYCLEGAN.jpg', x = 3.5) +
  draw_image('BASE-CYCLEGAN-MIX.jpg', x = 4.5) 

composite <- ggdraw(insert_xaxis_grob(graph, 
                                      pimage, 
                                      position = 'bottom',
                                      height  = grid::unit(0.5, 'null')))

pdf(file = 'INPUT.pdf',
    width = 8,
    height = 8)
print(composite)
dev.off()



