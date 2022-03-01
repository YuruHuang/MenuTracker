####################################################################
# Run this file to download/scrape data from all food outlets w NI #
#####################################################################

import os

from define_collection_wave import folder
from helpers import combo_PDFDownload, RunSpider, RunScript, java_PDF, greene_king_download

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

# 7. Starbucks - previously in PDF format
combo_PDFDownload('7_Starbucks', url='https://www.starbucks.co.uk/nutrition')
RunSpider('7_Starbucks', folder)

# 8. PizzaHut - PDF download
combo_PDFDownload(url='https://www.pizzahut.co.uk/restaurants/food/nutritional-information/', prex=
'https://www.pizzahut.co.uk', rest_name='8_Pizzahut')

# 9. Subway - both formats available, directly scrape from the website
RunSpider('9_Subway', folder)

# 10. Nandos
RunSpider('10_Nandos', folder)

# 11. Pizza Express -> PDF download
combo_PDFDownload(rest_name='11_PizzaExpress', keyword='ashx',
                  url='https://www.pizzaexpress.com/allergens-and-nutritionals',
                  prex='https://www.pizzaexpress.com')

# 12. Burger King -> Spider
RunSpider('12_BurgerKing', folder)

# 13. Pret -> Spider
RunSpider('13_Pret', folder)

# 14. Caffe Nero -> requests API
RunScript('14_CaffeNero', folder)

# 15. Wagamama -> Spider
RunSpider('15_Wagamama', folder)

# 16. Beefeater -> PDF
combo_PDFDownload(url='https://www.beefeater.co.uk/en-gb/allergy-nutrition',
                  rest_name='16_Beefeater', prex='https://www.beefeater.co.uk')

# 17. Brewers Fayre -> PDF
combo_PDFDownload(url='https://www.brewersfayre.co.uk/en-gb/allergy-nutrition',
                  rest_name='17_Brewersfayre', prex='https://www.brewersfayre.co.uk')

# 18. Sizzling Pubs
RunSpider('18_Sizzling', folder)

# 19. Ember Inns
RunSpider('19_EmberInns', folder)

# 20. Chef & Brewer Pub Co.
greene_king_download(rest_name='20_Chef', id=6145, url='https://www.chefandbrewer.com/', folder=folder)

# 21. Table Table
combo_PDFDownload(url='https://www.tabletable.co.uk/en-gb/allergy-nutrition', rest_name='21_TableTable',
                  prex='https://www.tabletable.co.uk')

# 22. Toby Cavery
RunSpider('22_Toby', folder)

# 23. Revolution
RunSpider('23_Revolution', folder)

# 24. Zizzi
combo_PDFDownload('24_Zizzi', url='https://www.zizzi.co.uk/menus')

# 25. Ask Italian
combo_PDFDownload(rest_name='25_Ask', url='https://www.askitalian.co.uk/allergens/')

# 26. Papa Johns - Nutrition calculators available only for US and Canada locations
combo_PDFDownload('26_PapaJohns', url='https://www.papajohns.co.uk/', prex='https://www.papajohns.co.uk')

# 27. Yates
RunSpider('27_Yates', folder)

# 28. Yo!Sushi -> lack carb and fibre information on websites -> PDF
combo_PDFDownload('28_Yosushi', url='https://yosushi.com/content/Allergen-and-Nutrition',
                  prex='https://yosushi.com')

# 29. All Bar One
RunSpider('29_AllBarOne', folder)

# 30. GBK
RunSpider('30_GBK', folder)
