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
# combo_PDFDownload('7_Starbucks', url='https://www.starbucks.co.uk/nutrition')
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
RunScript('14_CaffeNero')

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
# greene_king_download(rest_name='20_Chef', id=6145, url='https://www.chefandbrewer.com/', folder=folder)
RunSpider('20_ChefBrewer', folder)

# 21. Table Table
combo_PDFDownload(url='https://www.tabletable.co.uk/en-gb/allergy-nutrition', rest_name='21_TableTable',
                  prex='https://www.tabletable.co.uk')

# 22. Toby Cavery
RunSpider('22_Toby', folder)

# 23. Revolution
RunSpider('23_Revolution', folder)

# 24. Zizzi
# combo_PDFDownload('24_Zizzi', url='https://www.zizzi.co.uk/menus')
# started providing calorie only on web pages
RunSpider('24_Zizzi', folder)

# 25. Ask Italian
# combo_PDFDownload(rest_name='25_Ask', url='https://www.askitalian.co.uk/allergens/')
RunSpider('25_Ask', folder)

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

# 31. Flaming Grill
RunScript('31_FlamingGrill')

# 32. Loch Fyne seafood grill -> No nutrition available
# combo_PDFDownload('32_LochFyne', prex='https://www.lochfyneseafoodandgrill.co.uk',
#                   url='https://www.lochfyneseafoodandgrill.co.uk/allergens')
RunSpider('32_LochFyne', folder)

# 33. PAUL
RunSpider('33_Paul', folder)

# 34. Wimpy
RunSpider('34_Wimpy', folder)

# 35. Krispy Creme
RunSpider('35_KrispyKreme', folder)

# 36. Bills
RunSpider('36_Bills', folder=folder)

# 37. Walkabout
RunSpider('37_Walkabout', folder)

# 38. Itsu
RunSpider('38_Itsu', folder)

# 39. Ben & Jerry
RunSpider('39_BenJerry', folder)

# 40. Asda -> PDF format, randomly selected Asda
combo_PDFDownload('40_Asda', url='https://storelocator.asda.com/east-of-england/stevenage/monkswood-way/cafe')

# 41. Barburrito -> PDF
combo_PDFDownload(rest_name='41_Barburrito', url='https://www.barburrito.co.uk/menu')

# 42. Benugo
RunSpider('42_Benugo', folder)

# 43. Boost Juice
RunSpider('43_Boostjuice', folder)

# 44. Boswells
combo_PDFDownload('44_Boswell', 'https://boswellsgroup.com/menu/')

# 45. Brewhouse
combo_PDFDownload('45_Brewhouse', 'https://www.brewhouseandkitchen.com/bk-allergies/')

# 46. Cineworld
combo_PDFDownload('46_Cineworld', url='https://www.cineworld.co.uk/#/', prex='https://www.cineworld.co.uk',
                  keyword='jcr')

# 47. Coffee #1
combo_PDFDownload('47_Coffee1', 'https://www.coffee1.co.uk/food-nutritional-information/')

# 48. Common Rooms
RunSpider('48_CommonRooms', folder)

# 49. Cookhouse & Pub
combo_PDFDownload('49_CookhousePub', url='https://www.cookhouseandpub.co.uk/en-gb/allergy-nutrition?intcmp=footer',
                  prex='https://www.cookhouseandpub.co.uk', verify=False)

50.
Crussh -> terrible
website!
RunSpider('50_Crussh', json_=True, folder=folder)

# 51. Farmhouse Inns -> PDF
greene_king_download(rest_name='51_FarmhouseInns', id='5690', url='https://www.farmhouseinns.co.uk', folder=folder)

# 52. Five guys -> PDF
combo_PDFDownload(rest_name='52_FiveGuys', url='https://www.fiveguys.co.uk/nutrition')

# 53. Harvester
RunSpider('53_Harvester', folder)

# 54. Hungry Horse -> a greene king company
greene_king_download('54_HungryHorse', id='6347', url='https://www.hungryhorse.co.uk', folder=folder)

# 55. Joe & the Juice
RunSpider('55_JoeJuice', folder, json_=True)

# 56. Leon
RunSpider('56_Leon', folder)

# 57. greene king
greene_king_download('57_GreeneKing', id='8183', url='https://www.greeneking-pubs.co.uk', folder=folder)

# 58. Vue -> PDF
java_PDF('58_Vue', url='https://www.myvue.com/legal/nutritional-information',
         prex='https://www.myvue.com/legal/')

# 59. Ocean Cinema
java_PDF('59_Odeon', url='https://www.odeon.co.uk/experiences/food-drinks/food-and-drinks-facts-and-figures/',
         prex='https://www.odeon.co.uk',
         link_=False, xpath_="//p/a[contains(@title, 'Nutritional')]")

# 60. Marston's Pubs
combo_PDFDownload('60_Marstons', url='https://www.dragonflypubbasingstoke.co.uk/menus/')

# 61. Morrisons Cafe
RunScript('61_MorrisonsCafe')

# 62. Pho Cafe
combo_PDFDownload('62_Pho', url='https://www.phocafe.co.uk/menus/', prex='https://www.phocafe.co.uk')

# 63. Pieminister
RunSpider('63_Pieminister', folder)

# 64. Pure
RunScript('64_Pure')

# 65. Sainsbury Cafe
combo_PDFDownload('65_SainsburysCafe',
                  'https://www.sainsburys.co.uk/shop/gb/groceries/get-ideas/our-instore-services/--sainsburys-cafe',
                  prex='https://www.sainsburys.co.uk')

# 66. Soho Cafe
RunSpider('66_SohoCafe', folder)

# 67. Stonehouse Pizza
RunSpider('67_StonehousePizza', folder)

# 68. Tank and Paddle
RunSpider('68_TankPaddle', folder)

# 69. Tesco Cafe
RunSpider('69_TescoCafe', folder)

# 70. The Cornish Bakery
RunSpider('70_Cornish', folder)

# 71. Thomas the Baker
RunSpider('71_ThomasBaker', folder)

# 72. Tim Hortons
RunSpider('72_TimHortons', folder)

# 73. Top Golf -> PDF only
# tg_path = create_folder('73_TopGolf', folder)
# PDFDownloader(url='https://s3.topgolf.com/uploads/pdf/menus/topgolf-nutritional-information.pdf?v=20200131',
#               filePath=tg_path + '/top-golf-nutritional-information.pdf')
RunSpider('73_TopGolf', folder)

# 74. Town, Kitchen, and Pubs
RunSpider('74_TownKitchenPubs', folder)

# 75. Vintage Inns
RunSpider('75_VintageInns', folder)

# 76. Wasabi
RunScript('76_Wasabi')

# 77. Waterfields
RunSpider('77_Waterfields', folder, json_=True)

# 78. Birds Bakery
RunSpider('78_BirdsBakery', folder, json_=True)

# 79. Tortilla
RunScript('79_Tortilla')

# 80. Tossed
RunSpider('80_Tossed', folder)

# 81. Bella Italian
RunScript('81_BellaItalian')

# 82. Cafe Rouge
RunSpider('82_CafeRouge', folder)

# 83. Taco Bell
RunSpider('83_TacoBell', folder)

# 84. Coco di mama -> no NI anymore

# 85. The real greek
RunSpider('85_RealGreek', folder)

# 86. Honest Burger
combo_PDFDownload('86_HonestBurger', url='https://www.honestburgers.co.uk/allergy-information/', keyword='nutritional',
                  prex='https://www.honestburgers.co.uk/')

# 87. AMT
combo_PDFDownload('87_AMT', url='http://amtcoffee.co.uk/types/drinks/')
