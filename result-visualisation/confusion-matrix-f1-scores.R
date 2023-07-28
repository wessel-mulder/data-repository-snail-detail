library(ggplot2)
library(ggpubr)
library(dplyr)
library(scales)
library(gridExtra)
library(patchwork)
library(cowplot)
library(reshape2)
library(png)
library(magick)
library(grid)

### basics 
### accuracy data & binom
accuracies = read.csv('GEN_CLS_accuracies.csv')

harmonic_mean = function(vector){
  all = vector
  n = length(all)
  sum_inverse = sum(all^(-1))
  hm = n/sum_inverse
  print(hm)
}

#accuracies$F1 = (accuracies$precision + accuracies$recall)/2
accuracies$F1 = 2/(1/accuracies$precision + 1/accuracies$recall)
agg <- accuracies %>%
  group_by(species) %>%
  summarise(mean = mean(F1))
agg <- arrange(agg,desc(mean))

accuracies <- melt(accuracies, id.vars=c("model",'species','species_count'))
accuracies$model = as.factor(accuracies$model)
accuracies$species = factor(accuracies$species,levels = agg$species)

model_names = c('gen_a','gen_d','gen_v')

for(model_name in model_names){
    
    ### matrix data 
    sub_matrix = read.csv(paste0(model_name,'_gg_matrix.csv'))
    colnames(sub_matrix) = c('target','predict','n')
    
    ### make factors, arranged from highest to lowest mean
    
    sub_matrix$target = factor(sub_matrix$target,levels = agg$species)
    sub_matrix$predict = factor(sub_matrix$predict,levels = agg$species)
    
    sub_accuracies <- subset(accuracies, model %in% model_name)
  
    ### matrix plots
    matrix_p <- ggplot(sub_matrix, aes(x = target, y = predict, fill = n,label = n)) +
    geom_tile(color = 'white',
              lwd = 0.5,
              linetype = 1) +
    geom_text(aes(label = n),
              color = 'white',
              size = 3,
              fontface = 'bold') +
    theme_minimal() + 
    scale_y_discrete(limits = rev) +
    scale_x_discrete(position = 'top') +
    scale_fill_gradient(name = 'Number of predictions',
                        low = '#e7f5fe',
                        high = muted("red")) +
    theme(axis.text.x = element_text(angle = 67.5,
                                     face = 'italic',
                                     hjust = 0.05),
          axis.text.y = element_text(angle = 0,
                                     face = 'italic'),
          legend.position = 'bottom',
          legend.direction = 'horizontal') +
    labs(x = 'Ground truth',
         y = 'Model prediction')
    
  ### points plots
  sub_accuracies <- subset(sub_accuracies, variable %in% 'F1')
  mean = round(harmonic_mean(sub_accuracies$value),2)
  string = paste0('Macro F1-score = ',mean)
  
  if (model_name == 'gen_a'){
    img <- image_read('A.png')
    #img <- image_rotate(img,-90)
    img <- rasterGrob(img, interpolate=TRUE)
    y_pos = 5.75
    
  }else if (model_name == 'gen_d'){
    img <- image_read('D.png')
    img <- image_rotate(img,-90)
    img <- rasterGrob(img, interpolate=TRUE)
    title = 'Dorsal view'
    y_pos = 10.5
    
  }else if (model_name == 'gen_v'){
    img <- image_read('V.png')
    img <- image_rotate(img,-90)
    img <- rasterGrob(img, interpolate=TRUE)
    title = 'Ventral view'
    y_pos = 10.5
    
    
  }
    
  
  points_p <- ggplot(sub_accuracies, aes(col = species_count,y = species,x = value)) +
    theme_minimal() +
    geom_point() +
    annotate('text',x = 0.25, y=y_pos,label = string,
             size = 5, fontface = 'bold') + 
    scale_y_discrete(limits = rev) +
    scale_x_continuous(limits = c(0,1),
                       position = 'top',
                       name = 'F1-score per class') +
    scale_color_gradient(high = "#132B43",
                         low = "#56B1F7",
                         name = 'Number of original images') +
    theme(legend.position = 'bottom',
          legend.direction = 'horizontal',
          axis.ticks.y = element_blank(),
          axis.text.y = element_blank(),
          axis.title.y = element_blank()) +
    inset_element(img,left = 0.,right = 0.5, 
                  bottom = 0.3,top = 0.8) +

    theme(rect = element_rect(fill = 'transparent')) 
  
  if (model_name == 'gen_d'){
    lab = c('A','')
  }else if (model_name == 'gen_v'){
    lab = c('B','')
  }else if (model_name == 'gen_a'){
    lab = c('C','')}
    
  
  name = paste0(model_name,'_harmonic_macro.pdf')
  pdf(file = name,
      width = 14,
      height = 7)
  print(plot_grid(matrix_p,points_p,align = 'h',axis='bt',labels = lab))
  dev.off()
  
  print(paste0(model_name,' is finished'))
}



