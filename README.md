# MenuTracker

![image](https://user-images.githubusercontent.com/17410816/157275881-309938b3-3972-4b26-a97a-346583d95aad.png)


## 1. What is MenuTracker and the codebase? 
MenuTracker is a database that contains nutritional information served by large out-of-home chains in the UK. Large chain restaurants are defined as those with over 250 employees that provide nutritional information on their websites. The codebase of MenuTracker is written in Python, predominantly using <a href='https://scrapy.org/'> Scrapy framework</a>. We have developed scripts that allow **automatic download of nutritional PDFs** and **automated web scraping of nutritional information presented online**. For more information about the development of MenuTracker, please refer to our paper <a href='/'>here</a>. 

## 2. What data are collected by the scripts?

For each large out-of-home food chain, we collect `chain name`, `menu section`, `menu item name`, `menu item description`, `serving size`, and `nutritional information` where available. We collect the data quarterly and time-stamp every collection wave. Below is an example of McDonald's data collected during our March 2022 data collection wave (in json format): 

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

## 3. What is in this repo? 
-  `Master_Compile.py` is the master Python file you will need to run. Running the script initiates automatic download of nutritional PDFs and web scraping of nutritional information presented on the websites. 
-  `helpers.py` contains helpful Python functions and variables for MenuTracker data cllection. For example, `combo_PDFDownload` enables automatic download of nutritional PDF for the restaurant and creates a folder to save the PDF. 
-  `/Scrapy_spiders/Scrapy_spiders/spiders/~` contains individual web crawlers for chains, e.g., Nandos, Burger King, etc. Running individual spiders will initiate the web scraping of nutritional information for specific chains. *You may have to download the <a href='https://selenium-python.readthedocs.io/installation.html#drivers'>selenium webdriver </a> and change the path in order to download data for some chains. 
-  Other scripts, such as `4_Greggs.py`, also scrapes information for a specific chain, although not written in Python Scrapy framework. 

## 4. How do I use this codebase? 
### Step 1: Clone this repo 
### Step 2: Make changes where necessary
- Define your data collection wave in `define_collection_wave.py`
- Download the chrome driver and update the path where appropriate 
### Step 3: Run the code!
- Run `Master_Compile.py` for a full download, or run parts of it to download nutritional information for a specific chain.

*Disclaimer: use of our codebase is limited to non-commericial purposes. 

If you have any questions, or have ideas on how to automate the PDF data extraction, please feel free to reach me at Yuru.Huang@mrc-epid.cam.ac.uk.
