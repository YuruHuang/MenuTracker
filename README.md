# MenuTracker

![image](https://user-images.githubusercontent.com/17410816/157275881-309938b3-3972-4b26-a97a-346583d95aad.png)


## 1. What are MenuTracker and the codebase? 
MenuTracker is a database that contains nutritional information of menu items served by large out-of-home chains in the UK. Large chain restaurants are defined as those with over 250 employees that provide nutritional information on their websites. The codebase of MenuTracker is written in Python, predominantly using <a href='https://scrapy.org/'> Scrapy framework</a>. Some chains have nutritional information on HTML pages, while others only provide nutritional information in PDF format. Hence, we developed scripts that allow **automatic download of nutritional PDFs** (for PDFs only) and **automated web scraping of nutritional information presented online** (for HTML pages). For more information about the development of MenuTracker, please refer to our paper <a href='/'>here</a>. 

## 2. Why would I want to use MenuTracker?
If you are a researcher interested in the nutritional content of food served out-of-home, in particular how this changes over time in the UK. For researchers in other countries who wish to establish a similar nutritional database, MenuTracker is also a starting point for you to develop your own scripts.

## 3. What data are collected by the scripts?

For each large out-of-home food chain, we collect `chain name`, `menu section`, `menu item name`, `menu item description`, `serving size`, and `nutritional information` where available. We collect the data quarterly and time-stamp every collection wave. Below is an example of McDonald's data collected during our March 2022 data collection wave (in JSON format): 

```yaml
{
  "menu_id": 200432,
  "collection_date": "Dec-06-2021",
  "rest_name": "McDonalds UK",
  "menu_section": "Breakfast",
  "item_name": "Breakfast Roll with Ketchup",
  "item_description": "Delicious back bacon, our famous sausage patty, cheese and a freshly cracked free-range egg. All in a soft white roll with ketchup.",
  "servingsize": 215.4648132,
  "servingsizeunit": "g",
  "kcal": 496,
  "kcal_100": 230.2,
  "kj": 2082,
  "kj_100": 966.1,
  "protein": 31,
  "protein_100": 14.4,
  "carb": 42,
  "carb_100": 19.5,
  "sugar": 8.3,
  "sugar_100": 3.9,
  "fat": 22,
  "fat_100": 10.2,
  "satfat": 8,
  "satfat_100": 3.7,
  "fibre": 2.5,
  "fibre_100": 1.2,
  "salt": 2.7,
  "salt_100": 1.3,
  "ingredients": "Cheese Slice: Vegetarian Cheddar (51%) (MILK), Water, Vegetarian Cheese (9%) (MILK), Whey Powder (MILK), Butter (MILK), Emulsifying Salts (Trisodium Citrate, Citric Acid), Milk Proteins (MILK), Natural Cheese Flavouring (MILK), Salt, Colours  (Beta Carotene, Paprika Extract), Anti-Caking Agent (Sunflower Lecithin).TBCBuns - Breakfast: WHEAT Flour (contains Calcium Carbonate, Iron, Niacin, Thiamine), Water, Sugar, Rapeseed Oil, Fermented WHEAT Bran Sourdough, Salt, Yeast, Emulsifier (Mono- and Diacetyl Tartaric Acid Esters of Mono- and Diglycerides of Fatty Acids, Antioxidant (Ascorbic Acid).Allergy Advice:For allergens, including cereals containing gluten, see ingredients in BOLD.May also contain SESAME Seeds.No changeSausage Patty: Pork (97%), Salt, Dextrose, Herb and Herb Extract, Glucose Syrup, Spice, Yeast Extract.tbcBack Bacon: Pork, Salt, Preservative (Sodium Nitrite), Antioxidant (Sodium Ascorbate).Made with more than 140g of pork per 100g of finished product.TBCEggs - Free Range: Free Range EGG.Ketchup Bib: 66% Tomato Puree (equivalent to 184g Tomatoes\/100g Ketchup), Glucose-Fructose Syrup, Spirit Vinegar, Salt, Spice Extracts. TBC"
 }

```
## 4. How often will the scripts be updated? 
As chain websites change frequently, we will update the scripts every quarter. We currently have resources to continue updating the scripts (and collecting data) until September 2023. 

## 5. What is in this repo? 
There are two steps for obtaining MenuTracker data. First, we use Python scripts to collect restaurant nutritional information. Next, we standardise and compile all the data. 
### **Data Collection**:
-  `Master_Compile.py` is the master Python file you will need to run. Running the script initiates the automatic download of nutritional PDFs and web scraping of nutritional information presented on the websites. 
-  `helpers.py` contains helpful Python functions and variables for MenuTracker data collection. For example, `combo_PDFDownload` enables the automatic download of nutritional PDF for the restaurant and creates a folder to save the PDF. 
-  `/Scrapy_spiders/Scrapy_spiders/spiders/~` contains individual web crawlers for chains, e.g., Nandos, Burger King, etc. Running individual spiders will initiate the web scraping of nutritional information for specific chains.  
-  Other scripts, such as `4_Greggs.py`, also scrapes information for a specific chain, although not written in Python Scrapy framework. 
### **Data Cleaning**: 
- `DataMerge_MenuTracker.R` is the master R script that pulls and standardises all the restaurant nutritional information we collect from the previous step. 
- `Helpers.R` contains helpful customised R functions for cleaning, merging, and validation. 

***For restaurant nutritional information in PDF format, we use <a herf="https://tabula.technology">Tabula</a> or <a href="https://camelot-py.readthedocs.io/en/master/">Camelot</a> to extract data directly.***  

## 6. How do I use this codebase? 
### Step 1: Clone this repo 
### Step 2: Setting up the right virtual environment 
- All required Python packages are listed in the `requirement.txt` file. Install all the required packages. 
- Download the compatible <a href="https://sites.google.com/chromium.org/driver/">Chrome Driver</a> and update the driver path where appropriate.
### Step 3: Make changes where necessary
- Define your data collection wave in `define_collection_wave.py`
- Update relative/absolute paths where necessary. 
### Step 4: Run the code for data collection!
- Run `Master_Compile.py` for a full download, or run parts of it to download nutritional information for a specific chain.
### Step 5: Extract data from PDF
- If the chain you are interested in only provides nutritional information in PDF format, use Tabula or Camelot (linked above) to extract their data tables and save the csv in the corresponding folder.
### Step 6: Compile and standardise the data 
- Run `DataMerge_MenuTracker.R` file to merge the data if you need! 

Voila! Here you have the master file for one wave of MenuTracker data. 

***Disclaimer***: use of our codebase is limited to non-commercial purposes. We made every effort to minimise the burden on chain website owners and added download delays in our settings. 

If you have any questions, or have ideas on how to automate the PDF data extraction, please feel free to reach me at Yuru.Huang@mrc-epid.cam.ac.uk.
