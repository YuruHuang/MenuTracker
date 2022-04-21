#####################
# Helper functions  #
#####################

# This function adds menu sections for menu items after PDF conversion 
addMenuSection = function(folder_name, file_n){
  # 1. read data
  files= list.files(list.files(pattern=folder_name,full.names=TRUE),pattern='.csv',full.names = TRUE)
  dat = read_csv(files[file_n],guess_max = 1000)
  dat = data.table(dat)
  # 2. delete empty rows 
  dat = dat[!is.na(dat$item_name),]
  
  # 3. Get the menu sections 
  menu_section_index = which(is.na(dat$kj))
  
  # 4. menus: if indexes are two consecutive numbers, then the first one is the big menu 
  menu_section_index2 = menu_section_index[2:length(menu_section_index)]
  menu_section_indexDiff = menu_section_index2 - menu_section_index[1:length(menu_section_index)-1]
  big_menu_index = menu_section_index2[which(menu_section_indexDiff==1)]-1
  small_menu_index= setdiff(menu_section_index,big_menu_index)
  
  # 5. update menu sections
  menu_section_index = c(menu_section_index, dim(dat)[1])
  big_menu = ''
  small_menu =''
  for (i in 1:(length(menu_section_index)-1)){
    if (menu_section_index[i] %in% big_menu_index){
      big_menu = dat[menu_section_index[i],]$item_name
    }
    else{
      small_menu = dat[menu_section_index[i],]$item_name
    }
    menu_section = paste(big_menu,small_menu,sep=", ")
    lower = menu_section_index[i]
    upper = menu_section_index[i+1]
    dat[lower:upper,menu_sect:=menu_section]
  }
  
  # 6. Delete rows with menu sections
  dat = dat[!is.na(dat$kcal),]
  
  # 7. write the file
  write_csv(x=dat, files[file_n])
  }

## functions 
# replace trace with 0.05 
trace = function(x){gsub(pattern='trace|Trace',replacement='0.05',x)}
# clean numeric values 
clean_numeric = function(columns){
  columns = gsub(',','',columns) # replace , 8,256 --> 8256
  columns = gsub('<','',columns)
  columns = trace(columns)
  values = as.numeric(str_extract(pattern='[0-9]+([.][0-9]+)?',columns))
  return(values)
}
# convert non-numeric columns to numeric 
clean_columns = function(data){
  nutrient_list =  c('kj_100','kcal_100',
                     'kj','kcal','fat_100','fat','satfat_100',
                     'satfat','carb_100','carb','sugar_100','sugar','fibre_100',
                     'fibre','protein_100','protein','salt_100','salt',
                     'sodium','sodium_100','servingsize','starch')
  data %>% mutate_if(names(.) %in% nutrient_list, clean_numeric)
}
# read converted excel files from PDFs
pdf_convert = function(folder_name,rest_name,i=1){
  file= list.files(list.files(pattern=folder_name,full.names=TRUE),pattern='.csv',full.names = TRUE)
  data = read_csv(file[i])
  data$rest_name = rest_name
  data$collection_date = str_split(str_split(file,'/')[[1]][2],'_')[[1]][3]
  return(data)
}
pdf_combine = function(folder_name,rest_name){
  file = list.files(list.files(pattern=folder_name,full.names=TRUE),pattern='.csv',full.names = TRUE)
  data = lapply(file,read_csv)
  data = lapply(data, clean_columns)
  all = do.call('bind_rows',data)
  all$rest_name = rest_name
  all$collection_date = str_split(str_split(file,'/')[[1]][2],'_')[[1]][2]
  return(all)
}
# check Before Binding 
## 15/09/21: added more things to check 
check_bb = function(data){
  data_cols = colnames(data)
  basic_nutrients = c('kcal','kj','fat','sugar','carb','protein','salt','satfat','fibre')
  left = sum(!(basic_nutrients %in% data_cols))
  if (left !=0){
    print(paste(left, 'nutrients are not found'))
    print(basic_nutrients[!(basic_nutrients %in% data_cols)])
  }
  restaurant = unique(data$rest_name)
  if (nrow(data_all[data_all$rest_name==restaurant,])!=0){
    print(paste('This restaurant has already been added:',nrow(data_all[data_all$rest_name==restaurant,]),'records'))
  }
  if (sum(!(data_cols %in% colnames(data_all)))!=0){
    print(paste('Additional columns have been added:',data_cols[!(data_cols %in% colnames(data_all))]))
  }
  if (!grepl(pattern='[a-zA-Z]{3}-[0-9]{2}-[0-9]{4}', data$collection_date[1])){
    print('Dates format not correct!')
  }
  # check nutrient values 
  print(paste("Max sugar:", max(data$sugar,na.rm = TRUE),";","Max salt", max(data$salt,na.rm=TRUE),";",
              "Max kcal", max(data$kcal,na.rm=TRUE), ";", "Max protein", max(data$protein,na.rm=TRUE),";",
              "Max carb", max(data$carb,na.rm=TRUE),";",
              "Max fat", max(data$fat,na.rm=TRUE),";","","Max satfat", max(data$satfat,na.rm=TRUE)))
}

read_data = function(folder_name,i=1){
  files= list.files(list.files(pattern=folder_name,full.names=TRUE),pattern='.csv',full.names = TRUE)
  return(read_csv(files[i],guess_max = 1000))
}

# check duplicated column names 
dup_cols = function(data){
  col_names = colnames(data)
  col_names_s = gsub(' ','',tolower(col_names))
  if (length(col_names) == length(unique(col_names_s))){
    print("all column names are unique")}
  else{
    col_d1= col_names[which(duplicated(col_names_s,fromLast=TRUE))]
    col_d2 = col_names[which(duplicated(col_names_s))]
    data[[col_d1]] = with(data, coalesce(data[[col_d1]],data[[col_d2]]))
    data[[col_d2]] = NULL
    print(paste('Coalesced',col_d1,col_d2,sep=" "))
  }
  return (data)
}
