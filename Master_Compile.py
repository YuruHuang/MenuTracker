####################################################################
# Run this file to download/scrape data from all food outlets w NI #
#####################################################################

from helpers import headers,PDFDownloader,combo_PDFDownload,RunSpider,RunScript
import os
from datetime import date
import sys

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






