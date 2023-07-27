library(ggplot2)
library(dplyr)
library(stringr)

setwd('~/Desktop/')
data_total = read.csv('results_1207/models_best_update2.csv')
list <- strsplit(data_total$model,'-')
HQvect <- c()
CSvect <- c()
for (l in list){
  HQ <- strsplit(l[1],'_')[[1]][2]
  CS <- strsplit(l[2],'_')[[1]][2]
  HQvect <- append(HQvect,HQ)
  CSvect <- append(CSvect,CS)
}
data_total$HQ <- as.numeric(HQvect)
data_total$CS <- as.numeric(CSvect)
data_total$HQ <- factor(data_total$HQ,levels = sort(unique(data_total$HQ)))
data_total$CS <- factor(data_total$CS,levels = sort(unique(data_total$CS)))
data_total$value <- round(data_total$value,2)

data <- filter(data_total, stat %in% 'map')
tile <- ggplot(data, aes(x = HQ, y = CS, fill = value)) +
  geom_tile(width = 0.95,height=0.95)+
  scale_fill_gradient(low = "bisque2", high = "darkgoldenrod3") +
  labs(y = 'CS-crops',
       x = 'HQ-images',
       fill = 'mAP50')+
  geom_text(aes(label = value), color = "white", size = 4) +
  guides(fill = 'none') +
  theme_classic() +
  theme(axis.line = element_blank())
tile

pdf('grid.pdf',
    width = 6,
    height = 5)
print(tile)
dev.off()

data <- filter(data_total, stat %in% 'map')
point <- ggplot(data, aes(x = HQ, y = value)) +
  geom_boxplot()
point

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





