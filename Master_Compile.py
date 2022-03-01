####################################################################
# Run this file to download/scrape data from all food outlets w NI #
#####################################################################

import os

from define_collection_wave import folder
from helpers import combo_PDFDownload, RunSpider, RunScript, java_PDF

os.system('python define_collection_wave.py')

# 1. McDonald's
RunScript('1_McDonalds')

# 2. Wetherspoons
RunScript('2_Wetherspoons')

# 3. Costa Coffee
RunScript('3_CostaCoffee')

# 4. Greggs
RunScript('4_Greggs')

# 5. KFC - historically present their nutritional info in PDF format but recently made it available on their website
RunSpider('5_KFC', folder)

# 6. Domino - PDF download
java_PDF('6_Dominos', url='https://corporate.dominos.co.uk/allergens-nutritional')

# 7. Starbucks - PDF download
combo_PDFDownload('7_Starbucks', url='https://www.starbucks.co.uk/nutrition')

# 8. PizzaHut - PDF download
combo_PDFDownload(url='https://www.pizzahut.co.uk/restaurants/food/nutritional-information/', prex=
'https://www.pizzahut.co.uk', rest_name='8_Pizzahut')

# 9. Subway - both formats available, directly scrape from the website
RunSpider('9_Subway')

# 10. Nandos
RunSpider('10_Nandos')

# 11. Pizza Express -> PDF download
combo_PDFDownload(rest_name='11_PizzaExpress', keyword='ashx',
                  url='https://www.pizzaexpress.com/allergens-and-nutritionals',
                  prex='https://www.pizzaexpress.com')

# 12. Burger King -> Spider
RunSpider('12_BurgerKing', folder)

# 13. Pret -> Spider

# 14. Caffe Nero -> Spider

# 15. Wagamama -> Spider
