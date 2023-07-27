library(ggplot2)
library(ggpubr)
library(cowplot)
library(jpeg)
library(patchwork)
library(magick)
library(ggnewscale)

setwd('~/Desktop/')
data_total = read.csv('models_best_update2.csv')
### BASE 

# mAP, BIO and BULS across models -----------------------------------------------------------
stats =  c('map')
new_data <- subset(data_total, stat %in% stats)

all <- ggplot(new_data, aes(x = image_number, y = value))+
  geom_line() +
  facet_wrap(~image_type,scales = 'free_x',)+
  theme_minimal() 
print(all)

cs <- subset(new_data, image_type %in% 'CS')
colnames(cs) <- c('model','stat','value','type','CS_number')
hq <- subset(new_data, image_type %in% 'HQ')
colnames(hq) <- c('model','stat','value','type','HQ_number')


try <- ggplot()+
  geom_line(data = cs, aes(x = value, y = CS_number, color = type))+
  geom_line(data = hq, aes(x = value, y = HQ_number, color = type))+
  scale_y_continuous(limits = c(0,100),
                     sec.axis = sec_axis(~hq$HQ_number))
print(try)

name = paste0(names[it],'.pdf')
print(name)
pdf(file = name,
    width = 8,
    height = 8)
print(copy)
dev.off()





