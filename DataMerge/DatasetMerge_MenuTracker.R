####################################################
## merge and standarize collected restaurant data ##
####################################################
library(data.table)
library(tidyverse)
library(stringr)
library(tidyr)
library(dplyr)
library(readxl)
library(openxlsx)

source('Helpers.R')

rm(list = ls())

wd = '/Users/huangyuru/PycharmProjects/MenuTracker/June_collection_2022' # fill in your working dictionary

setwd(wd)


# 1. Mcdonald's 
mcdonalds_file = list.files(list.files(pattern='mcdonalds',full.names=TRUE,ignore.case = TRUE),pattern='.csv',full.names = TRUE)
mcdonalds = read_csv(mcdonalds_file)
mcdonalds$collection_date = str_split(list.files(pattern='mcdonalds',ignore.case=TRUE),pattern='_')[[1]][3]
mcdonalds$rest_name = 'McDonalds UK'

# calculate the serving sizes based on the density and per serving values
mcdonalds$servingsize = mcdonalds$energy_kcal_Quantity/mcdonalds$energy_kcal_100_g_per_product*100
mcdonalds$servingsizeunit ='g'

mcdonalds_select = mcdonalds %>% select ('item_id','collection_date','rest_name','Product_Category','Product_Name','Product_Description',
                                         'servingsize','servingsizeunit','energy_kcal_Quantity','energy_kcal_100_g_per_product',
                                         'energy_kJ_Quantity','energy_kJ_100_g_per_product','protein_Quantity',
                                         'protein_100_g_per_product','carbohydrate_Quantity','carbohydrate_100_g_per_product',
                                         'sugars_Quantity','sugars_100_g_per_product',
                                         'fat_Quantity','fat_100_g_per_product',
                                         'saturated_fat_Quantity','saturated_fat_100_g_per_product',
                                         'fibre_Quantity','fibre_100_g_per_product',
                                         'salt_Quantity','salt_100_g_per_product','Product_Ingredients')

names<-c('menu_id','collection_date','rest_name','menu_section','item_name','item_description','servingsize',
         'servingsizeunit','kcal','kcal_100','kj','kj_100','protein','protein_100','carb','carb_100',
         'sugar','sugar_100','fat','fat_100','satfat','satfat_100','fibre','fibre_100','salt','salt_100','ingredients')
colnames(mcdonalds_select) =names 

#filename = paste('mcdonalds',mcdonalds$collection_date[1],'standarized_formerge.csv',sep='_')
#write_csv(mcdonalds_select,filename)

# 2. wetherspoon
wetherspoon = read_data('Wetherspoon')
wetherspoon$collection_date = str_split(list.files(pattern='wetherspoon',ignore.case = TRUE),pattern='_')[[1]][3]
wetherspoon$rest_name = 'Wetherspoon'


wetherspoon_select = wetherspoon %>% select ('ProductId','collection_date','rest_name','Category','Name','Summary',
                                             'Calories','Protein',
                                         'Carbohydrates', 'Sugar','Fat','SaturatedFat',
                                         'Fibre','Salt','Ingredients','Allergens','IsNew')

names<-c('menu_id','collection_date','rest_name','menu_section','item_name','item_description',
         'kcal','protein','carb','sugar','fat',
         'satfat','fibre','salt','ingredients','allergens','new')
colnames(wetherspoon_select) =names
check_bb(wetherspoon_select)
wetherspoon_select$menu_id = as.character(wetherspoon_select$menu_id)

# create data_all (merged data.frame)
data_all = bind_rows(mcdonalds_select,wetherspoon_select)


# 3. Costa coffee
costa_file = list.files(list.files(pattern='costa',full.names=TRUE,ignore.case = TRUE),pattern='.csv',full.names = TRUE)
costa = read_csv(costa_file)
costa$collection_date = str_split(list.files(pattern='costa',ignore.case = TRUE),pattern='_')[[1]][3]
costa$rest_name = 'Costa Coffee'

#modify the item names with milk, take away or in store, and size
costa$item_name = gsub("NA,|, NA", "",paste(costa$Product_Name,costa$Size,costa$Milk,sep=', '))
#for each item, create two rows, one for In-Store, and the other for Takeaway
costa_withinstore = costa[costa$ServingSize_In_Store!='N',]
instore = data.frame(collection_date = costa_withinstore$collection_date, rest_name = costa_withinstore$rest_name,
                     menu_section = costa_withinstore$Category,
                     item_name = paste(costa_withinstore$item_name,'In Store',sep=', '),item_description=costa_withinstore$Product_Description,
                     servingsize=str_extract(pattern='[0-9]+[.]?[0-9]?',costa_withinstore$ServingSize_In_Store),servingsizeunit = str_extract(pattern='[A-Za-z]+',costa_withinstore$ServingSize_In_Store),
                     kcal = costa_withinstore$`Energy (kcal)_In-Store`,kcal_100 = costa_withinstore$`Energy (kcal)_Per 100g/ml`,
                     kj = costa_withinstore$`Energy (kJ)_In-Store`, kj_100 = costa_withinstore$`Energy (kJ)_Per 100g/ml`,
                     protein = costa_withinstore$`Protein (g)_In-Store`, protein_100=costa_withinstore$`Protein (g)_Per 100g/ml`,
                     carb = costa_withinstore$`Carbohydrate (g)_In-Store`, carb_100 = costa_withinstore$`Carbohydrate (g)_Per 100g/ml`,
                     sugar = costa_withinstore$`of which is sugars (g)_In-Store`, sugar_100 = costa_withinstore$`of which is sugars (g)_Per 100g/ml`,
                     fat = costa_withinstore$`Fat (g)_In-Store`, fat_100 = costa_withinstore$`Fat (g)_Per 100g/ml`,
                     satfat = costa_withinstore$`of which is saturates (g)_In-Store`, satfat_100 = costa_withinstore$`of which is saturates (g)_Per 100g/ml`,
                     salt = costa_withinstore$`Salt (g)_In-Store`, salt_100 = costa_withinstore$`Salt (g)_Per 100g/ml`
)

# not all items have takeaway values 
sum(costa$ServingSize_Take_Out=='N')
costa_withtakeaway = costa[costa$ServingSize_Take_Out != 'N',]
takeaway = data.frame(collection_date = costa_withtakeaway$collection_date, rest_name = costa_withtakeaway$rest_name,
                    menu_section = costa_withtakeaway$Category,
                    item_name = paste(costa_withtakeaway$item_name,'Take Out',sep=', '),item_description=costa_withtakeaway$Product_Description,
                    servingsize=str_extract(pattern='[0-9]+[.]?[0-9]?',costa_withtakeaway$ServingSize_Take_Out),servingsizeunit = str_extract(pattern='[A-Za-z]+',costa_withtakeaway$ServingSize_Take_Out),
                    kcal = costa_withtakeaway$`Energy (kcal)_Take-Out`,kcal_100 = costa_withtakeaway$`Energy (kcal)_Per 100g/ml`,
                    kj = costa_withtakeaway$`Energy (kJ)_Take-Out`, kj_100 = costa_withtakeaway$`Energy (kJ)_Per 100g/ml`,
                    protein = costa_withtakeaway$`Protein (g)_Take-Out`, protein_100=costa_withtakeaway$`Protein (g)_Per 100g/ml`,
                    carb = costa_withtakeaway$`Carbohydrate (g)_Take-Out`, carb_100 = costa_withtakeaway$`Carbohydrate (g)_Per 100g/ml`,
                    sugar = costa_withtakeaway$`of which is sugars (g)_Take-Out`, sugar_100 = costa_withtakeaway$`of which is sugars (g)_Per 100g/ml`,
                    fat = costa_withtakeaway$`Fat (g)_Take-Out`, fat_100 = costa_withtakeaway$`Fat (g)_Per 100g/ml`,
                    satfat = costa_withtakeaway$`of which is saturates (g)_Take-Out`, satfat_100 = costa_withtakeaway$`of which is saturates (g)_Per 100g/ml`,
                    salt = costa_withtakeaway$`Salt (g)_Take-Out`, salt_100 = costa_withtakeaway$`Salt (g)_Per 100g/ml`
)

costa_select = bind_rows(instore, takeaway)
dim(costa_select)
View(costa_select)

costa_select$servingsize=as.numeric(costa_select$servingsize)
check_bb(costa_select)
data_all = bind_rows(data_all,costa_select)
dim(data_all)

# 4. Greggs 
## the script was rewritten 
greggs_file = list.files(list.files(pattern='greggs',full.names=TRUE,ignore.case = TRUE),pattern='.csv',full.names = TRUE)
greggs = read_csv(greggs_file)
colnames(greggs)[9:24] = c('menu_section','allergens','kcal','kcal_100','fat','fat_100','satfat','satfat_100',
                            'sugar','sugar_100','salt','salt_100','protein','protein_100',
                            'carb','carb_100')
greggs = greggs[,2:24]
check_bb(greggs)
data_all = bind_rows(data_all,greggs)

# 5. KFC
kfc = read_data('KFC')
colnames(kfc) = c('rest_name','collection_date','item_name','menu_section','allergens',
                  'vegan','vegetarian','servingsize','kj','kcal','fat','satfat','carb',
                  'sugar','protein','salt')
check_bb(kfc)
data_all$servingsize = as.character(data_all$servingsize)
data_all = bind_rows(data_all, kfc)

# 6. Dominos
dominos = pdf_combine('Dominos','Domino\'s Pizza')
dominos = data.table(dominos)
dominos[is.na(item_name),item_name := paste(pizza_name,crust_type,size,sep=',') ]
dominos$pizza_name=NULL
dominos$crust_type = NULL
dominos$size = NULL
check_bb(clean_columns(dominos))
data_all<-bind_rows(data_all,dominos)
dim(data_all)

# 7. Starbucks 
starbucks = read_data('Starbucks')
starbucks = separate(starbucks, 'energy', into=c('kcal','kj'))
# starbucks$caffeine=NULL
starbucks = data.table(starbucks)
colnames(starbucks)[14] <- 'satfat'
colnames(starbucks)[15]<-'carb'
# servingsize 
#starbucks[starbucks$servingsize %in% c('Grande','Dopio','Short','Mini','Tall'),item_name:=paste(item_name,servingsize,sep=', ')]
#starbucks[starbucks$servingsize =='1 Piece', servingsize:=NA]
starbucks = clean_columns(starbucks)
# add size and milk choice to the item name 
starbucks$...1=NULL
check_bb(starbucks)
starbucks[,item_name:=paste(item_name,size,milk, sep= ', ')]
starbucks$item_name = gsub(starbucks$item_name,pattern=' NA,',replacement='')
starbucks$item_name = gsub(starbucks$item_name,pattern=' NA',replacement='')
starbucks$size=NULL
starbucks$milk = NULL
starbucks$servingsize = starbucks$servingSize
starbucks$servingSize = NULL
data_all = bind_rows(data_all,starbucks)

# 8. Pizzahut
pizzahut_new = pdf_convert('Pizzahut','Pizza Hut')
check_bb(pizzahut_new)
pizzahut_new$servingsize = as.character(pizzahut_new$servingsize)
data_all = bind_rows(data_all,pizzahut_new)

# 9. Subway
subway = read_data('Subway')
colnames(subway)<-c('collection_date','rest_name','menu_section','menu_id',
                    'item_name','item_description','servingsize','kj','kcal','fat','satfat',
                    'carb','sugar','fibre','protein','salt')
subway$menu_id = as.character(subway$menu_id)
check_bb(subway)
subway$servingsize = as.character(subway$servingsize)
data_all<-bind_rows(data_all,subway)

# 10. Nandos 
nandos_file = list.files(list.files(pattern='nandos',full.names=TRUE,ignore.case = TRUE),pattern='.csv',full.names = TRUE)
nandos = read_csv(nandos_file)
nandos$collection_date = str_split(list.files(pattern='nandos',ignore.case=TRUE),pattern='_')[[1]][3]
nandos$rest_name = 'Nandos'

nandos_select = nandos %>% select ('collection_date','rest_name','Product Category','Product Name','Product Description',
                                   'Product Price', 'Energy (kcal) per serving','Energy (kj) per serving',
                                   'Fat per serving','Saturated fat per serving','Carbohydrates per serving',
                                   "Sugar per serving","Fibre per serving","Protein per serving",
                                   "Salt per serving")
nandos_select2 = nandos_select %>% mutate_at(vars('Energy (kcal) per serving','Energy (kj) per serving',
                            'Fat per serving','Saturated fat per serving','Carbohydrates per serving',
                            "Sugar per serving","Fibre per serving","Protein per serving",
                            "Salt per serving"), function(x) as.numeric(str_extract(pattern='[0-9]+[.]?[0-9]?',x)))
names<-c('collection_date','rest_name','menu_section','item_name','item_description','price','kcal','kj','fat',
         'satfat','carb','sugar','fibre','protein','salt')
colnames(nandos_select2) =names
check_bb(nandos_select2) 
data_all = bind_rows(data_all,nandos_select2)

# 11. Puzza Express 
pizzaexp = pdf_convert('PizzaExpress','PizzaExpress')
check_bb(pizzaexp)
#pizzaexp$rest_name ='PizzaExpress'
data_all<-bind_rows(data_all,pizzaexp)

#12. Burgerking 
burgerking_file = list.files(list.files(pattern='burgerking',full.names=TRUE,ignore.case=TRUE),pattern='.csv',full.names = TRUE)
burgerking = read_csv(burgerking_file)
check_bb(burgerking)
data_all = bind_rows(data_all,burgerking)

# 13. Pret a Manger
pret_file = list.files(list.files(pattern='pret',full.names=TRUE,ignore.case=TRUE),pattern='.csv',full.names = TRUE)
pret = data.table(read_csv(pret_file))
colnames(pret)[14:31] = c('kj_100','kj',
                          'kcal_100','kcal','fat_100','fat','satfat_100','satfat',
                          'carb_100','carb',
                          'sugar_100','sugar','fibre_100','fibre',
                          'protein_100','protein',
                          'salt_100','salt')

pret$servingsize = as.character(pret$kcal/pret$kcal_100*100)
pret[!is.na(servingsize),servingsizeunit:='g']
pret$menu_id = unlist(lapply(pret$url,function(x) {str_split(x,'/')[[1]][6]}))
check_bb(pret)
data_all$menu_id = as.character(data_all$menu_id)
data_all = bind_rows(data_all,pret)

# 14. Caffe Nero 
nero_file = list.files(list.files(pattern='nero',full.names=TRUE,ignore.case=TRUE),pattern='.csv',full.names = TRUE)
nero = read_csv(nero_file)
nero
colnames(nero) = c('delete','collection_date','rest_name',"item_name", "item_description", "vegeterian",
                   "menu_section", "kj_100", "kj" , "kj_uom", "kcal_100", "kcal", "kcal_uom",
                   "fat_100", "fat", "fat_uom", "carb_100", "carb", "carb_uom", "protein_100", 
                   "protein", "protein_uom", "satfat_100", "satfat", "satfat_uom", 
                   "sugar_100",  "sugar", "sugar_uom",  "fibre_100", "fibre", "fibre_uom",
                   "salt_100","salt", "salt_uom", 
                   "sodium_100", "sodium", "sodium_uom")
table(nero$menu_section)
nero$servingsize = as.character(nero$kcal/nero$kcal_100*100)
nero = data.table(nero)
nero[is.infinite(servingsize),servingsize:=NA]
nero[!is.na(servingsize),servingsizeunit:='g']
#nero2$Christmas=ifelse(nero$menu_section=='festive',1,0)
#sum(nero2$Christmas)
# delete all columns with _umo 
nero[,delete:=NULL]
nero[,grep(colnames(nero),pattern='_uom'):=NULL]
check_bb(nero)
data_all = bind_rows(data_all,nero)
dim(data_all)

#15. wagamama 
wagamama = read_data('Wagamama')
wagamama
colnames(wagamama) <- c('rest_name','collection_date','item_name','item_description','allergens',
                        'kj','kj_100','protein','protein_100','carb','carb_100','sugar',
                        'sugar_100','fat','fat_100','satfat','satfat_100','fibre','fibre_100',
                        'sodium','sodium_100','salt','salt_100')
wagamama = clean_columns(wagamama)
wagamama$kcal = wagamama$kj/4.1868 
wagamama$kcal_100 = wagamama$kj_100/4.1868
wagamama_unique = data.table(wagamama[!duplicated(wagamama),])
wagamama_unique$servingsize = as.character(wagamama_unique$kj/wagamama_unique$kj_100*100)
wagamama_unique[!is.na(wagamama_unique$servingsize),servingsizeunit:='g']
check_bb(wagamama_unique)
data_all = bind_rows(data_all,wagamama_unique)
dim(data_all)

# 16. Beefeater 
beefeater = pdf_combine('Beefeater','Beefeater Grill')
check_bb(beefeater)
data_all<-bind_rows(data_all,beefeater)

# 17. Brewers Fayre
# clean files
addMenuSection(folder_name ='Brewers',file_n=3)
# addMenuSection(folder_name ='Brewers',file_n=2)
brewers = pdf_combine('Brewers','Brewers Fayre')
check_bb(brewers)
data_all<-bind_rows(data_all,brewers)

#18. Sizzling pubs
sizzling = read_data('Sizzling')
sizzling2 = sizzling %>% mutate_at(vars('kcal','kj','fat',
                                       'satfat','carb','sugar','protein','salt'), function(x) as.numeric(str_extract(pattern='[0-9]+([.][0-9]+)?',gsub(pattern=',',replacement='',x))))
check_bb(sizzling2)
data_all = bind_rows(data_all,sizzling2)

#19. Ember Inns
ember_file = list.files(list.files(pattern='ember',full.names=TRUE,ignore.case=TRUE),pattern='.csv',full.names = TRUE)
ember = read_csv(ember_file)
ember2 = ember %>% mutate_at(vars('kcal','kj','fat',
                                        'satfat','carb','sugar','protein','salt'), function(x) as.numeric(str_extract(pattern='[0-9]+([.][0-9]+)?',gsub(pattern=',',replacement='',x))))

#ember2$Christmas=ifelse(grepl(ember2$menu_section,pattern='festive|christmas',ignore.case = TRUE),1,0)
check_bb(ember2)
data_all = bind_rows(data_all,ember2)
dim(data_all)

# 20. Chef and Brewer 
chef = read_data('Chef')
check_bb(chef)
data_all<-bind_rows(data_all,chef)

# 21. Table table --> has the exact same menu as the brewers fayre (!)
table = pdf_convert('TableTable','Table Table')
check_bb(table)
data_all <- bind_rows(data_all,table)

#22.Toby
toby = read_data('Toby')
toby2 = toby %>% mutate_at(vars('kcal','kj','fat',
                                'satfat','carb','sugar','protein','salt'), function(x) as.numeric(str_extract(pattern='[0-9]+([.][0-9]+)?',gsub(pattern=',',replacement='',x))))
check_bb(toby2)
data_all = bind_rows(data_all,toby2)

# 23. Revolution Bars
revolution = read_data('Revolution')
colnames(revolution) = c('collection_date','rest_name','menu_section','item_name','item_description',
                         'price','allergens','kj','fat','kcal','sodium','satfat','carb','sugar','protein')
revolution = clean_columns(revolution)
# delete the inaccurate rows
#revolution3 = revolution[(!is.na(revolution$item_name))& revolution$kcal!=0 & !is.na(revolution$kcal),]
check_bb(revolution)
revolution$salt = revolution$sodium*2.54
data_all = bind_rows(data_all,revolution)
dim(data_all)

# 24. zizzi
zizzi = read_data('Zizzi')
colnames(zizzi)<-c('collection_date','rest_name',
                   'menu_reference','menu_section','item_name',
                   'menu_id','kcal','item_description','price','dietary')
check_bb(zizzi)
zizzi$menu_id = as.character(zizzi$item_id)
zizzi$price = as.character(zizzi$price)
zizzi = clean_columns(zizzi)
data_all<-bind_rows(data_all,zizzi)

# 25. ask 
ask = read_data('Ask')
colnames(ask)<-c('collection_date','rest_name',
                   'menu_reference','menu_section','item_name',
                   'menu_id','kcal','item_description','price','dietary')
ask$menu_id = as.character(ask$menu_id)
ask$price = as.character(ask$price)
ask = clean_columns(ask)
check_bb(ask)
data_all<-bind_rows(data_all,ask)

# 26. Papa Johns 
papa = pdf_convert('Papa','Papa John\'s')
papa<-data.table(papa)
#pizza: 3 slices, small: whole pizza
papa[grepl('- Small',item_name)]
slice = colnames(papa)[grepl(pattern='slice',colnames(papa))]
serving = gsub('_slice','',slice)
for (i in 1:length(slice)){
  papa[grepl('- Small',item_name), serving[i]:=get(slice[i])*6]
  papa[(!(grepl('- Small',item_name))) & (!is.na(kcal_slice)), serving[i]:=get(slice[i])*3]
}

papa2<-papa %>% select("item_name","kcal_100","kj_100","protein_100", "carb_100","sugar_100",
                       "fat_100", "satfat_100", "fibre_100","sodium_100","salt_100","kcal" 
                       ,"kj","protein","carb","sugar", "fat","satfat", "fibre", "sodium",
                       "salt","rest_name", "collection_date")
check_bb(papa2)
data_all<-bind_rows(data_all,papa2)

#27. Yates 
yates_file = list.files(list.files(pattern='yates',full.names=TRUE,ignore.case=TRUE),pattern='.csv',full.names = TRUE)
yates = read_data('Yates')
head(yates)
check_bb(yates)
data_all<-bind_rows(data_all,yates)

# 28. Yo!Sushi
yosushi = pdf_combine('Yosushi','YO! Sushi')
check_bb(yosushi)
colnames(yosushi)[colnames(yosushi) == 'mono'] <- 'monofat'
colnames(yosushi)[colnames(yosushi) == 'poly'] <- 'polyfat'
yosushi$salt = yosushi$sodium*2.54/1000
data_all<-bind_rows(data_all,yosushi)
dim(data_all)

#29. All Bar One: no nutritional information???? recaptured on March 26
allbarone_file = list.files(list.files(pattern='allbarone',full.names=TRUE,ignore.case=TRUE),pattern='.csv',full.names = TRUE)
allbarone = read_data('AllBarOne')
# View(allbarone)
#allbarone$Christmas = ifelse(grepl(allbarone$menu_section,pattern='festive|christmas',ignore.case = TRUE),1,0)
allbarone2 = allbarone  %>% mutate_at(vars('kj','kcal','fat',
                                             'satfat','carb','sugar','protein','salt'), function(x) as.numeric(str_extract(pattern='[0-9]+([.][0-9]+)?',gsub(pattern=',',replacement='',x))))
check_bb(allbarone2)
data_all<-bind_rows(data_all,allbarone2)

# 30. GBK 
gbk = read_data('GBK')
colnames(gbk)<-c('collection_date','rest_name','menu_section','item_name',
                 'item_description','kcal','protein','carb','sugar','fat',
                 'satfat','salt','delete')
gbk$delete=NULL
gbk = clean_columns(gbk)
check_bb(gbk)
# gbk2$collection_date = str_split(str_split(gbk_file,'/')[[1]][2],'_')[[1]][2]
data_all<-bind_rows(data_all,gbk)

# 31. Flaming Grill 
flaming = pdf_combine('Flaming',"Flaming Grill Pub Co.")
check_bb(flaming)
flaming$menu_section = paste(flaming$menu_reference, flaming$menu_section,sep=",")
flaming$menu_reference = NULL
#flaming$kcal = as.character(flaming$kcal)
data_all<-bind_rows(data_all,flaming)

# 32. Loch Fyne
loch = read_data('Loch')
loch = clean_columns(loch)
check_bb(loch)
data_all = bind_rows(data_all, loch)

# 33. PAUL
paul = read_data('Paul')
colnames(paul)<-c('collection_date','rest_name','item_name',
                  'item_description','price',
                  'allergens','servingsize','kj','kcal','fat',
                  'satfat','transfat','unsatfat','cholestrol',
                  'sodium','salt','carb','sugar','fibre','protein',
                  'kj_100','kcal_100','fat_100','satfat_100','transfat_100',
                  'unsatfat_100','cholestrol_100','sodium_100','salt_100',
                  'carb_100','sugar_100','fibre_100','protein_100')
# comma needs to be replaced with . for example 77,3 -> 77.3 not 773
nutrient_list =  c('kj','kcal','fat',
                   'satfat','transfat','unsatfat','cholestrol',
                   'sodium','salt','carb','sugar','fibre','protein',
                   'kj_100','kcal_100','fat_100','satfat_100','transfat_100',
                   'unsatfat_100','cholestrol_100','sodium_100','salt_100',
                   'carb_100','sugar_100','fibre_100','protein_100')
paul2 = paul %>% mutate_if(names(.) %in% nutrient_list, function(x){as.numeric(gsub(',','.',x))})
paul2 = data.table(paul2)
paul2[!is.na(servingsize),servingsizeunit:='g']
View(paul2)
check_bb(paul2)
paul2$servingsize = as.character(paul2$servingsize)
data_all<-bind_rows(data_all,paul2)
dim(data_all)

# 34. Wimpy
wimpy_file = list.files(list.files(pattern='wimpy',full.names=TRUE,ignore.case=TRUE),pattern='.csv',full.names = TRUE)
wimpy = read_data('Wimpy')
colnames(wimpy)[5]<-'menu_id'
wimpy$menu_id<-as.character(wimpy$menu_id)
check_bb(wimpy)
data_all<-bind_rows(data_all,wimpy)
dim(data_all)

# 35. Krispy
krispy = read_data('Krispy')
colnames(krispy)[23]<-'allergens'
check_bb(krispy)
data_all = bind_rows(data_all, krispy)

# 36. Bills
bills = read_data('Bills')
colnames(bills) <- c('collection_date','rest_name','menu_section','item_name',
                     'item_description','kcal')
bills = clean_columns(bills)
check_bb(bills)
data_all<-bind_rows(data_all,bills)

#37 Walkabout
walkabout_file = list.files(list.files(pattern='walkabout',full.names=TRUE,ignore.case=TRUE),pattern='.csv',full.names = TRUE)
walkabout = read_data('Walkabout')
check_bb(walkabout)
data_all<-bind_rows(data_all,walkabout)

#38. itsu
itsu  = read_data('Itsu')
itsu2 = itsu  %>% mutate_at(vars('kcal','fat',
                                           'satfat','carb','sugar','protein','fibre','salt'), function(x) as.numeric(str_extract(pattern='[0-9]+([.][0-9]+)?',gsub(pattern=',',replacement='',x))))
check_bb(itsu2)
colnames(itsu2)[14]<-'allergens'
data_all<-bind_rows(data_all,itsu2)

#39. Ben Jerry
ben = read_csv(list.files(list.files(pattern='Ben',full.names=TRUE),pattern='joined.*csv',full.names = TRUE))
# delete duplicates 
colnames(ben)<- gsub(colnames(ben),pattern='.x',replacement='')
check_bb(ben)
colnames(ben)[colnames(ben) == 'nutrition_url'] <- 'url'
ben$servingsize<-as.character(ben$servingsize)
data_all <- bind_rows(data_all, ben)

#40.asda 
asda = pdf_convert('Asda','Asda')
# for whole pizza items, calculate the nutrient values based on 3 slices
asda = data.table(asda)
asda = clean_columns(asda)
asda$kj_perslice = as.numeric(gsub('kJ','',asda$kj_perslice))
asda$kcal_perslice = as.numeric(gsub('kcal','',asda$kj_perslice))

asda[!is.na(kcal_perslice),kcal:=kcal_perslice*3]
asda[!is.na(kcal_perslice),kj:=kj_perslice*3]
asda[grepl('whole', tolower(item_name)),kcal:=kcal/2]
asda[grepl('whole', tolower(item_name)),kj:=kj/2]
asda[,c('kcal_perslice','kj_perslice'):=NULL]
check_bb(asda)
#colnames(asda)[7]<-'price'
data_all = bind_rows(data_all,asda)

# 41. Barburrito
barburrito = pdf_convert('burrito','Barburrito')
check_bb(barburrito)
barburrito$size=NULL
data_all = bind_rows(data_all,barburrito)

#42. Benugo
benugo = read_data('Benugo')
check_bb(benugo)
data_all$vegetarian = as.character(data_all$vegetarian)
data_all = bind_rows(data_all,benugo)

# 43. boost juice
boostjuice = read_data('Boostjuice')
# first strip off all the units for 
boostjuice2 =boostjuice %>% mutate_at(vars('kj','fat','carb','fibre','protein','satfat','sugar','sodium'), function(x) as.numeric(str_extract(pattern='[0-9]+([.][0-9]+)?',x)))
# sodium to salt 
boostjuice2$salt = boostjuice2$sodium*2.54/1000
# servingsizes 
boostjuice2 = boostjuice2 %>%
  separate(servingsize, c("size","servingsize", "servingsizeunit"), " ")
boostjuice2$item_name = paste(boostjuice2$item_name,boostjuice2$size,sep=", ")
boostjuice2$size=NULL
boostjuice2$servingsize = as.numeric(boostjuice2$servingsize)
boostjuice2$kcal = boostjuice2$kj*0.2388 
check_bb(boostjuice2)
boostjuice2$servingsize = as.character(boostjuice2$servingsize)
data_all = bind_rows(data_all, boostjuice2)

# 44. boswells
boswell = pdf_combine('Boswell','BOSWELL')
check_bb(boswell)
data_all = bind_rows(data_all, boswell)

# 45.Brewhouse
brewhouse = pdf_convert('Brewhouse','Brewhouse and Kitchen')
check_bb(brewhouse)  
data_all = bind_rows(data_all,brewhouse)

# 46. Cineworld
path = list.files(list.files(pattern='Cineworld',full.names=TRUE),pattern='.xlsx',full.names = TRUE)
cineworld = lapply(excel_sheets(path), read_excel, path = path)
cineworld_all = do.call(plyr::rbind.fill,cineworld)
cineworld_all$sodium= as.numeric(trace(cineworld_all$sodium))*100
cineworld_all$collection_date = str_split(str_split(path,'/')[[1]][2],'_')[[1]][3]
cineworld_all$rest_name= 'Cineworld'
cineworld_all = clean_columns(cineworld_all)
cineworld_all$servingsizeunit = str_extract(cineworld_all$servingsize,'g|oz|ml')
cineworld_all$servingsize =str_extract(cineworld_all$servingsize,'[0-9]+([.][0-9]+)?')
check_bb(cineworld_all)
data_all = bind_rows(data_all,cineworld_all)

# 47. coffee1 
# refer to coffee1.R for data manipulation of the food items 
coffee1 = pdf_combine('Coffee1','Coffee #1')
check_bb(coffee1)
coffee1$servingsize = as.character(coffee1$servingsize)
data_all = bind_rows(data_all,coffee1)

# 48. Common Rooms 
commonrooms = read_data('Common')
check_bb(commonrooms)
data_all = bind_rows(data_all,commonrooms)

# 49. cookhouse --> the same as brewers fayre!
cookhouse = pdf_convert('Cookhouse','Cookhouse & Pub')
check_bb(cookhouse)
data_all = bind_rows(data_all,cookhouse)

# 50. Crussh
crussh = data.table(read_data('Crussh'))
crussh_cols = colnames(crussh)
clean_cols = gsub('per portion', 'per serving',gsub("[()]", "", gsub('\\*','',tolower(crussh_cols)))) #lower, replace *,remove (), and per portion = perserving
clean_cols = str_replace_all(pattern='\\s',replacement='',clean_cols)
clean_cols = gsub('_perservingsml','_sml',gsub('_perservingmed','_med',clean_cols))
clean_cols = gsub('_large','_lrg',gsub('_small','_sml',clean_cols))
clean_cols = gsub('sugars','sugar',clean_cols)
clean_cols = gsub('carbohydrates','carbohydrate',clean_cols)
clean_cols = gsub('saturatedfat','saturates',clean_cols)
clean_cols = gsub('g_','_',clean_cols)
clean_cols = gsub('_100ml','_100g',clean_cols)
sum(duplicated(clean_cols))
colnames(crussh) = clean_cols
crussh[,...1:=NULL]

# coalesce columns with the same names
crussh_df = data.frame(crussh)
crussh_df = crussh_df %>% mutate_at(vars(-one_of('rest_name','collection_date','menu_section',
                                                 'item_name','item_description','price','allergens')),function(x) as.numeric(trace(gsub(',','.',gsub('<','',x)))))
crussh_new = data.frame(x=1:nrow(crussh))
for (col_name in unique(colnames(crussh))){
  allnames = colnames(crussh_df)
  samenames_index = which(grepl(col_name,allnames))
  samenames =allnames[samenames_index]
  if ((length(samenames_index)>1)) {
    data_col = crussh_df[,samenames_index] # variables with the same name 
    assign(col_name, do.call(coalesce,data_col))
  }
  else{
    assign(col_name,crussh_df[[col_name]])
  }
  crussh_new = bind_cols(crussh_new, get(col_name))
}

colnames(crussh_new) <- c('id',unique(colnames(crussh)))

# now for items with other sizes, create new columns for them
sizes = c('2oz','1oz','med','lrg','sml')
newrows = data.frame()
for (size in sizes){
  rows = crussh_new[!is.na(get(paste('energykcal_',size,sep=''))),]
  select_cols = c(colnames(crussh_new)[ grepl(size,colnames(crussh_new))],'rest_name','collection_date','menu_section',
                  'item_name','item_description','price','allergens',colnames(crussh_new)[ grepl('_100g',colnames(crussh_new))])
  col_names = gsub(size,'perserving',select_cols)
  select_rows = rows[,select_cols]
  colnames(select_rows) = col_names
  select_rows$size = size
  newrows = bind_rows(newrows,select_rows)
}

crussh_new = bind_rows(crussh_new,newrows)
# update item names - add size
crussh_new = data.table(crussh_new)
crussh_new[!is.na(size),item_name:=paste(item_name,size,sep=', ')]
# delete items without kcal_serving
crussh_new = crussh_new[!is.na(energykcal_perserving)]
# delete extra columns
crussh_new = crussh_new[,2:22]
colnames(crussh_new) = c('rest_name','collection_date','menu_section','item_name',
                         'item_description','price','allergens','kcal_100','kcal','fat_100',
                         'fat','satfat_100','satfat','carb_100','carb','sugar_100','sugar',
                         'protein_100','protein','salt_100','salt')
check_bb(crussh_new)
data_all = bind_rows(data_all,crussh_new)

# 51. Farmhouse 
farmhouse = pdf_combine('Farmhouse','Farmhouse Inns')
check_bb(farmhouse)
farmhouse$menu_section = gsub('\r',' ',farmhouse$menu_section)
farmhouse$menu_reference = gsub('\r',' ',farmhouse$menu_reference)
farmhouse$menu_section = paste(farmhouse$menu_reference,farmhouse$menu_section,sep=', ')
farmhouse$menu_reference= NULL
data_all = bind_rows(data_all, farmhouse)

# 52. Five guys
fiveguys = pdf_convert('FiveGuys','FIVE GUYS')
check_bb(fiveguys)
fiveguys = clean_columns(fiveguys)
data_all = bind_rows(data_all,fiveguys)

# 53. Harvester 
harvester = read_data('Harvester')
harvester = harvester %>% mutate_at(vars('kj','kcal','protein',
                                         'carb','sugar','fat','satfat',
                                         'salt'), function(x) as.numeric(str_extract(pattern='[0-9]+([.][0-9]+)?',gsub(pattern=',','',x))))
check_bb(harvester)
data_all = bind_rows(data_all, harvester)

# 54. Hungry Horse
# server error pdf does not work
hungry = pdf_convert('HungryHorse','Hungry Horse')
check_bb(hungry)
hungry$menu_section = gsub('\r',' ',hungry$menu_section)
hungry$menu_reference = gsub('\r',' ',hungry$menu_reference)
hungry$menu_section = paste(hungry$menu_reference,hungry$menu_section,sep=', ')
hungry$menu_reference= NULL
data_all = bind_rows(data_all,hungry)

# 55. Joe & the Juice 
joejuice = read_data('Joe')
colnames(joejuice)<- c('X1','collection_date','rest_name',
                       'menu_section','item_name','item_description',
                       'price','allergens','kj','protein','kcal','carb',
                       'fibre','sugar','fat','satfat',
                       'sodium')
joejuice$X1 = NULL
joejuice = clean_columns(joejuice)
joejuice$salt = joejuice$sodium*2.54/1000
check_bb(joejuice)
data_all$servingsize = as.character(data_all$servingsize)
data_all = bind_rows(data_all,joejuice)

# 56. Leon
leon = read_data('Leon')
colnames(leon)<- c('rest_name','collection_date','item_name',
                   'item_description','allergens','ingredients','kcal',
                   'protein','carb','sugar','fat','satfat','mono_unsatfat','poly_unsatfat',
                   'salt','glycemic_index','servingsize','fibre')
check_bb(leon)
leon$servingsizeunit = 'g'
leon$servingsize = as.character(leon$servingsize)
data_all = bind_rows(data_all,leon)

# 57. greene King
greeneking = pdf_convert('GreeneKing','Greene King')
check_bb(greeneking)
greeneking$menu = gsub('\r',' ',greeneking$menu)
greeneking$menu_section = paste(greeneking$menu,greeneking$menu_section,sep=', ')
greeneking$menu= NULL
data_all = bind_rows(data_all, greeneking)

# 58. Vue 
vue = pdf_convert('Vue','VUE ENTERTAINMENT')
check_bb(vue)
vue = clean_columns(vue)
data_all = bind_rows(data_all, vue)

# 59. Odeon: pre-packaged items not included ()
addMenuSection('Odeon')
odeon = data.table(pdf_convert('Odeon','ODEON'))
odeon$size = str_extract(pattern='[0-9]+oz|[0-9]+g',odeon$item_name)
odeon$servingsizeunit = str_extract(pattern='oz|g',odeon$size)
odeon$servingsize = as.numeric(str_extract(pattern='[0-9]+',odeon$size))
odeon$size= NULL
check_bb(odeon) #  some numbers not correct 
odeon = clean_columns(odeon) 
odeon$servingsize = as.character(odeon$servingsize)
# add menu_sections
data_all = bind_rows(data_all, odeon)

# 60. Martons 
martons = yosushi_cleaner('Marstons',"Marston\'s")
colnames(martons) = c('item_name','kcal','kcal_percent','kj','kj_percent','fat','fat_percent','satfat',
                      'satfat_percent','carb','carb_percent','sugar','sugar_percent','protein','protein_percent',
                      'fibre','fibre_percent','salt','salt_percent','rest_name','collection_date')
martons = clean_columns(martons)
check_bb(martons)
data_all = bind_rows(data_all,martons)

# 61. Morrisons 
morrisons = read_data('Morrisons')
check_bb(morrisons)
morrisons$price = as.character(morrisons$price)
colnames(morrisons)[6]<- 'menu_id'
morrisons$...1=NULL
morrisons$menu_id = as.character(morrisons$menu_id)
data_all = bind_rows(data_all, morrisons)

# 62. pho
pho = data.table(pdf_convert('Pho','Pho'))
pho = clean_columns(pho)
check_bb(pho)
data_all = bind_rows(data_all, pho)

# 63. Pieminister
pieminister = read_data('Pieminister')
colnames(pieminister) = c('rest_name','collection_date','menu_section','item_name',
                          'item_description','ingredients','url',
                          'kj','kj_100','kcal','kcal_100','fat','fat_100','satfat',
                          'satfat_100','carb','carb_100','sugar','sugar_100','protein',
                          'protein_100','salt','salt_100')
check_bb(pieminister)
pieminister = clean_columns(pieminister)
data_all = bind_rows(data_all,pieminister)

# 64. Pure
pure = read_data('Pure')
colnames(pure) =  c('delete','rest_name','collection_date','menu_section','menu_id','item_name',
                    'item_description',
                    'price','allergens','ingredients','kj','kj_100',
                    'kcal','kcal_100','fat','fat_100','satfat','satfat_100',
                    'carb','carb_100','sugar','sugar_100','fibre','fibre_100',
                    'protein','protein_100','salt','salt_100','servingsize','servingsizeunit')
pure = clean_columns(pure)
check_bb(pure)  
pure$servingsizeunit = as.character(pure$servingsizeunit)
pure[!is.na(pure$servingsize),'servingsizeunit']<-'g'
pure$delete=NULL
pure$menu_id<-as.character(pure$menu_id)
pure$servingsize <- as.character(pure$servingsize)
pure$price <- as.character(pure$price)
data_all = bind_rows(data_all, pure)  

# 65. sainsbury
sainsburys = pdf_convert('Sainsburys','Sainsbury\'s')
check_bb(sainsburys)
sainsburys= clean_columns(sainsburys)
data_all = bind_rows(data_all, sainsburys)


# 66. Soho
soho = read_data('Soho')
soho2 = soho %>% separate(`Energy per 100g`, into=c('kj_100','kcal_100'),sep='/')  
soho2 = soho2 %>% separate(`Energy per serving`, into=c('kj','kcal'),sep='/')  
colnames(soho2)<-c('collection_date','rest_name','menu_section','item_name',
                   'item_description','allergens','kj_100','kcal_100',
                   'kj','kcal','fat_100','fat','satfat_100',
                   'satfat','carb_100','carb','sugar_100','sugar','fibre_100',
                   'fibre','protein_100','protein','salt_100','salt')
soho2 =soho2 %>% mutate_at(vars('kj_100','kcal_100',
                                'kj','kcal','fat_100','fat','satfat_100',
                                'satfat','carb_100','carb','sugar_100','sugar','fibre_100',
                                'fibre','protein_100','protein','salt_100','salt'),function(x) as.numeric(str_extract(pattern='[0-9]+([.][0-9]+)?',x)))
View(soho2)
check_bb(soho2)
data_all = bind_rows(data_all,soho2)

# 67.stonehouse
stonehouse = read_data('Stonehouse')
stonehouse = clean_columns(stonehouse)
check_bb(stonehouse)
data_all = bind_rows(data_all,stonehouse)

# 68. tank 
tank = read_data('Tank')
tank = clean_columns(tank)
check_bb(tank)
data_all = bind_rows(data_all, tank)

# 69. tesco - a new column to reserve range values 
tesco = read_data('Tesco')
tesco$kcal_c = tesco$kcal
tesco$kcal = as.numeric(gsub(pattern="kcal", replacement="",tesco$kcal_c))
check_bb(tesco)
data_all = bind_rows(data_all,tesco)

# 70. cornish
cornish = read_data('Cornish')
colnames(cornish)<-c('collection_date','rest_name','item_name','item_description',
                     'price','ingredients','allergens','url','servingsize',
                     'kj_100','kj','kcal_100','kcal','fat_100','fat',
                     'satfat_100','satfat','carb_100','carb','sugar_100',
                     'sugar','protein_100','protein','salt_100','salt')
cornish$servingsizeunit='g'
cornish$servingsize = as.character(cornish$servingsize)
check_bb(cornish)
data_all = bind_rows(data_all,cornish)

# 71. Thomas the baker 
thomas = data.table(read_data('Thomas'))
thomas = thomas %>% separate(`Energy_100`, into=c('kj_100','kcal_100'),sep='/')  
thomas$servingsize = as.numeric(str_extract(thomas$servingsize,'[0-9]+(\\.[0-9]+)?'))
thomas[!is.na(Fat_100),servingsizeunit := 'g']
colnames(thomas) = c( "collection_date" ,"rest_name","menu_section",
                      "item_name" , "price", "item_description", "allergens",
                      "ingredients", "servingsize", "url",
                      "kj_100","kcal_100" ,"fat_100",
                      "satfat_100", "carb_100", "sugar_100",
                      "protein_100", "salt_100" ,"servingsizeunit" )
thomas = clean_columns(thomas)
# calculate the serving sizes based on nutrient density 
thomas$kj = thomas$kj_100*thomas$servingsize/100
thomas$kcal =thomas$kcal_100*thomas$servingsize/100
thomas$fat = thomas$fat_100*thomas$servingsize/100
thomas$satfat = thomas$satfat_100*thomas$servingsize/100
thomas$carb = thomas$carb_100*thomas$servingsize/100
thomas$sugar = thomas$sugar_100*thomas$servingsize/100
thomas$protein = thomas$protein_100*thomas$servingsize/100
thomas$salt = thomas$salt_100*thomas$servingsize/100
check_bb(thomas)
thomas$servingsize =as.character(thomas$servingsize)
data_all = bind_rows(data_all, thomas)

# 72. Tim Hortons 
tim = data.table(read_data('Tim'))
# fix some errors
tim[grepl(Energy_percent,pattern='kJ'),Energy_perserving:=Energy_percent]
tim[grepl(Energy_percent,pattern='kJ'),Energy_percent:=NA]
tim = tim %>% separate(`Energy_perserving`, into=c('kj','kcal'),sep='/')  
# if rows only have kcal 
tim[grepl(kj,pattern='kcal'), kcal:=kj]
tim[grepl(kj,pattern='kcal'), kj:=NA]
tim$servingsizeunit = str_extract(tim$servingsize,'oz|g')
tim$servingsize = as.numeric(str_extract(tim$servingsize,'[0-9]+(\\.[0-9]+)?'))

colnames(tim) = c( "collection_date", "rest_name","menu_section" , "menu_id",                      
                   "item_name", "servingsize", "allergens" ,'kj','kcal','kcal_percent',
                   'fat','fat_percent','satfat_percent','carb','carb_percent','sugar',
                   'sugar_percent','fibre','protein','protein_percent','salt','servingsizeunit')
tim = clean_columns(tim)
data_all$menu_id = as.character(data_all$menu_id)
tim$servingsize = as.character(tim$servingsize)
check_bb(tim)
tim$satfat = 20* as.numeric(gsub('%',"",tim$satfat_percent))/100
data_all = bind_rows(data_all,tim)

# 73. top golf 
topgolf = read_data('TopGolf')
colnames(topgolf) = c('item_name','kcal','kj','fat','satfat','carb',
                      'sugar','fibre','protein','salt','collection_date',
                      'rest_name','menu_section','allergens')
topgolf = clean_columns(topgolf)
check_bb(topgolf)
data_all = bind_rows(data_all,topgolf)

# 74. Town, Kitchen and Pubs
townkitchen = read_data('Town')
check_bb(townkitchen)
data_all = bind_rows(data_all,townkitchen)

# 75. Vintage Inns
vintageinns = read_data('Vintage')
check_bb(vintageinns)
vintageinns = clean_columns(vintageinns)
data_all= bind_rows(data_all,vintageinns)

# 76. Wasabi
wasabi = read_data('Wasabi')
check_bb(wasabi)
wasabi$...1=NULL
data_all = bind_rows(data_all,wasabi)

# 77. waterfields
waterfields = read_data('Waterfields')
waterfields$...1 = NULL
waterfields_d = dup_cols(waterfields)
colnames(waterfields_d) = c("collection_date","rest_name","menu_section",
                            "item_name","item_description",
                            "kj","kj_100","kcal","kcal_100",'fat','fat_100',
                            'satfat','satfat_100','monofat','monofat_100',
                            'polyfat','polyfat_100','carb','carb_100',
                            'sugar','sugar_100','starch','starch_100',
                            'fibre','fibre_100','protein','protein_100',
                            'salt','salt_100','sodium','sodium_100'
)
check_bb(waterfields_d)
data_all = bind_rows(data_all,waterfields_d)


# 78. Birds Bakery
birds = read_data('Birds')
birds$...1 = NULL
colnames(birds) = c('collection_date','rest_name','menu_section','menu_id','item_name',
                    'allergens','vegetarian','kj_100','kcal_100','fat_100','satfat_100',
                    'carb_100','sugar_100','fibre_100','protein_100','salt_100','delete')
colnames(birds)
birds$delete = NULL
check_bb(birds)
birds$menu_id<- as.character(birds$menu_id)
data_all = bind_rows(data_all, birds)


# 79. tortilla
tortilla = read_data('Tortilla')
colnames(tortilla) = c('delete','component_name','kcal','kj','fat','satfat','carb',
                       'sugar','fibre','protein','salt','allergens','may contain','collection_date',
                       'rest_name','menu_id','step','item_name')
tortilla$delete=NULL
tortilla$component = 'Yes'
check_bb(tortilla)
tortilla = clean_columns(tortilla)
tortilla$menu_id = as.character(tortilla$menu_id)
data_all = bind_rows(data_all, tortilla)


# 80. Tosssed
tossed = read_data('Tossed')
colnames(tossed) = c('rest_name','collection_date', 'item_name','item_description',
                     'menu_section','kcal','fat','satfat','protein','salt','kj','carb',
                     'sugar','fibre')
tossed = clean_columns(tossed)
check_bb(tossed)
data_all = bind_rows(data_all, tossed)

# 81. Bella 
bella = read_data('Bella')
bella$...1 = NULL
colnames(bella) = c('rest_name','collection_date','item_name',
                    'item_description','menu_section','kcal',
                    'protein','carb','sugar','fat','satfat','salt')
bella = clean_columns(bella)
check_bb(bella)
data_all = bind_rows(data_all, bella)

# 82. Cafe rouge 
rouge = read_data('CafeRouge')
colnames(rouge) = c('collection_date','rest_name','menu_section','item_name','item_description',
                    'menu_reference','kcal','protein','carb','sugar','fat','satfat','salt')
rouge = clean_columns(rouge)
check_bb(rouge)
data_all = bind_rows(data_all, rouge)

# 83. Taco
taco_bell = read_data('Taco')
colnames(taco_bell) = c('collection_date','rest_name','menu_id','menu_section','item_name',
                        'allergens','ingredients','servingsize',
                        'kcal','kcal_100',
                        'fat','fat_100','satfat','satfat_100',
                        'sodium','sodium_100','carb','carb_100',
                        'sugar','sugar_100',
                        'protein','protein_100')

colnames(taco_bell) = c('collection_date','rest_name','menu_id','menu_section',
                        'item_name','allergens','ingredients','servingsize','kcal','kcal_100','fat_calorie','fat_calorie_100',
                        'fat','fat_100','satfat','satfat_100','transfat','transfat_100','polyfat','polyfat_100',
                        'monofat','monofat_100','cholesterol','cholesterol_100','sodium','sodium_100',
                        'carb','carb_100','fibre','Fibre_100','sugar','sugar_100',
                        'sugar_alcohol','sugar_alcohol_100','protein','protein_100',
                        'vitaminA','vitaminA_100','vitaminC','vitaminC_100','calcium','calcium_100',
                        'iron','iron_100','potassium_2018','potassium_2018_100','caffeine','caffeine_100','vitaminD','vitaminD_100','added_sugar','added_sugar_100')
# convert sodium to salt 
check_bb(taco_bell)
taco_bell$menu_id<-as.character(taco_bell$menu_id)
taco_bell$servingsize <- as.character(taco_bell$servingsize)
taco_bell$salt = taco_bell$sodium*2.54/1000
taco_bell$salt_100 = taco_bell$sodium_100*2.54/1000
taco_bell$transfat = as.numeric(taco_bell$transfat)
taco_bell$transfat_100 = as.numeric(taco_bell$transfat_100)
data_all = bind_rows(data_all,taco_bell)

# 84. Coco di mama
coco = read_data('Coco')
colnames(coco)<-c('collection_date','rest_name',
                 'menu_reference','menu_section','item_name',
                 'menu_id','kcal','item_description','price','dietary')
coco$menu_id = as.character(coco$menu_id)
coco$price = as.character(coco$price)
coco= clean_columns(coco)
check_bb(coco)
data_all<-bind_rows(data_all,coco)

# 85. realgreek 
realgreek = data.table(read_data('Greek'))
realgreek$kcal = str_extract(pattern='[0-9]+',realgreek$dietary)
realgreek$vegetarian = gsub('?\\(.[0-9]+.*(k)?(K)?cal(\\))?','',realgreek$dietary)  
realgreek[,dietary:=NULL]  
check_bb(realgreek)
realgreek$kcal = as.numeric(realgreek$kcal )
data_all$vegetarian = as.character(data_all$vegetarian)
data_all = bind_rows(data_all, realgreek)

# 86. Honest burgers 
honest = pdf_convert('HonestBurger','Honest Burgers')
check_bb(honest)
data_all = bind_rows(data_all,honest)

# 87. AMT
amt = pdf_convert('AMT','AMT Coffee')
amt$price = as.character(amt$price)
check_bb(amt)
data_all = bind_rows(data_all,amt)



# rouge = pdf_convert('rouge','Café Rouge')
# rouge = clean_columns(rouge)
# check_bb(rouge)
# data_all = bind_rows(data_all, rouge)


data_all = fread('MenuTracker_Jun2022_060622.csv')
fwrite(data_all,'MenuTracker_Jun2022_080822.csv')




