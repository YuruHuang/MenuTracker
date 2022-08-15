######################
#  fix some dates    #
######################

# pdf_convert function previously get the dates as position 2, but with the indexes the position should be 3
# some restaurants have their names in the collection_date column instead of the dates 

dates_to_be_fixed = unique(data_all$collection_date)
dates_to_be_fixed = dates_to_be_fixed[!grepl(pattern='[a-zA-Z]{3}-[0-9]{2}-[0-9]{4}', dates_to_be_fixed)]
data_all = data.table(data_all)

for (rest in dates_to_be_fixed){
  #1. read the dates from this restaurant 
  file= list.files(list.files(pattern=rest,full.names=TRUE),pattern='.csv',full.names = TRUE)
  if (rest=='Cineworld'){
    file = list.files(list.files(pattern=rest,full.names=TRUE),pattern='.xlsx',full.names = TRUE)
  }
  # correct dates
  collection_date_rp = str_split(str_split(file,'/')[[1]][2],'_')[[1]][3]
  # 2. Replace the collection date 
  data_all[collection_date==rest,collection_date:=collection_date_rp]
  # 3. Confirm 
  print(paste('I have changed dates for',rest, 'to ->',collection_date_rp,sep=' '))
}
