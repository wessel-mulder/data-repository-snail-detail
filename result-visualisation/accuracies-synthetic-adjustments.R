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



