import os
import re
import urllib
from datetime import date
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from define_collection_wave import folder

# Define user headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Accept': 'application/json'
}


# function to remove html tags
def cleanhtml(raw_html):
    '''
    This function removes html tags from raw html texts
    :param raw_html:
    :return: cleaned text file
    '''
    if not raw_html:
        return raw_html
    else:
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext


# function: download a PDF file
def PDFDownloader(url, filePath, verif=True):
    '''
    This function takes in the URL to download a PDF and downloads the PDF file
    :param url: the URL for the PDF
    :param filePath: file path to store the PDF
    :param verif: True or False. Default is set to True. If the PDF download is unsuccessful because of the verification error, set the verif to False
    :return: saves the PDF file
    '''
    r = requests.get(url, stream=True, verify=verif, headers=headers)
    with open(filePath, "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
            # writing one chunk at a time to a pdf file
            if chunk:
                pdf.write(chunk)

# Downloading multiple PDFs
def combo_PDFDownload(rest_name, url, keyword='pdf', prex=None, verify=True):
    '''
    This function identifies all PDFs available for download and save all of them
    :param rest_name: the name of the restaurant
    :param url: URL for downloading the PDFs
    :param keyword: keyword for identifying the PDF download link. The default is set to 'pdf'
    :param prex: if the PDF download link does not contain domain link, add the domain url here
    :param verify: True or False. whether to allow authentication
    :return: multiple downloaded PDFs
    '''
    path = folder + '/' + rest_name + '_' + date.today().strftime("%b-%d-%Y")
    os.mkdir(path)
    html = requests.get(url, headers=headers, verify=verify)
    soup = BeautifulSoup(html.text, 'html.parser')
    urls = soup.select(f"a[href*={keyword}]")
    for url in urls:
        url_link = url.get('href')
        if 'https://' not in url_link and 'http://' not in url_link:
            if url_link[0] != '/':
                url_link = '/' + url_link
            url_link = prex + url_link
        filename = url_link.split('/')[-1]
        if filename[-3:] != 'pdf':
            filename = filename + '.pdf'
        filePath = path + '/' + filename
        print(url_link)
        print(filePath)
        PDFDownloader(url=url_link, filePath=filePath)
    print('finished downloading pdfs for ' + rest_name)


# Download PDFs with Selenium
def java_PDF(rest_name, url, prex=None):
    path = create_folder(rest_name, folder)
    s = Service(web_browser_path)
    browser = webdriver.Chrome(service=s)
    browser.get(url)
    # links that contain PDF
    links = [link.get_attribute('href') for link in browser.find_elements(by=By.PARTIAL_LINK_TEXT, value='Download')]
    for url_link in links:
        browser.get(url_link)
        sleep(5)
        if 'https://' not in url_link and 'http://' not in url_link:
            if url_link[0] != '/':
                url_link = '/' + url_link
            url_link = prex + url_link
        filename = url_link.split('/')[-1]
        if filename[-3:] != 'pdf':
            filename = filename + '.pdf'
        filePath = path + '/' + filename
        print(url_link)
        print(filePath)
        PDFDownloader(url=url_link, filePath=filePath)
    browser.quit()


def create_folder(rest_name, folder):
    '''
    Creates a folder for each restaurant
    :param rest_name: the name of the restaurant folder
    :return: a new folder for the restaurant will be created
    '''
    path_temp = './' + folder + '/' + rest_name + '_' + date.today().strftime("%b-%d-%Y")
    os.mkdir(path_temp)
    return path_temp

# function: create a folder and run the spider
def RunSpider(spidername, folder, json=False):
    '''
    This function allows the spiders to run and saves the spider outputs
    :param spidername: the name of the spider you want to run
    :param folder: folder for the data collection wave
    :param json: Default is False (file saving as csv).
    :return: spider output saved in csv or json
    '''
    absolute_path = '/Users/huangyuru/PycharmProjects/MenuTracker'
    path = create_folder(spidername, folder)
    os.chdir(absolute_path + '/Scrapy_spiders')
    if json is True:
        os.system("scrapy crawl " + spidername + " -o " + absolute_path + path[1:]+ '/' + spidername + '_items.json')
    else:
        os.system("scrapy crawl " + spidername + " -o " + absolute_path + path[1:] + '/' + spidername + '_items.csv')
    os.chdir(absolute_path)
    print('finished scraping ' + spidername)

# function: run the script for a restaurant (requests)
def RunScript(rest_name):
    try:
        os.system('python ' + rest_name + '.py')
        print('Successfully scraped ' + rest_name)
    except:
        print('Issues with' + rest_name + '. Please Review')


# Selenium Path
web_browser_path = '/Users/huangyuru/PycharmProjects/MenuStatUK/chromedriver'


# Downloading PDF for Greene King companies
def greene_king_download(rest_name, id, url, folder):
    path = create_folder(rest_name, folder)
    menus = requests.get(f'https://menu.greeneking-pubs.co.uk/{id}').json().get('data').get('menus')
    for menu in menus:
        menu_name = urllib.parse.quote(menu.get('name'))
        get_menu_url = f'{url}/umbraco/api/menu/getmenus?id={id}&name={menu_name}'
        url_pdfs = requests.get(get_menu_url).json().get('data').values()
        for url_pdf in url_pdfs:
            if url_pdf is not None:
                url_pdf = url + url_pdf
                path_temp = path + '/' + url_pdf.split('/')[-1]
                PDFDownloader(url_pdf, path_temp)
