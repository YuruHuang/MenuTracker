import json
import os
import re
from ssl import OP_SINGLE_DH_USE
from tkinter import E
import urllib
from datetime import date
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from define_collection_wave import folder
import platform

# Define paths 
root_path = 'C:\\Users\\yh459\\OneDrive - University of Cambridge\\MenuTracker\\MenuTracker'
web_browser_path = os.path.join(root_path, 'chromedriver.exe')


# windows or osx
if platform.system() == 'Windows':
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    operation_system = 'Windows'
else:
    headers = {'User-Agent': 'Mozilla/5.0 (Linuxintosh; Intel Linux OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15'}
    operation_system = 'Linux'


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

# function to create a folder for each restaurant
def create_folder(rest_name, folder):
    '''
    Creates a folder for each restaurant
    :param rest_name: the name of the restaurant folder
    :return: a new folder for the restaurant will be created
    '''
    rest_folder  =  rest_name + '_' + date.today().strftime("%b-%d-%Y")
    path = os.path.join(folder, rest_folder)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

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
    path = create_folder(rest_name, folder)
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
            if '.pdf' in filename: 
                filename = filename.split('?')[0]
            else: 
                filename = filename + '.pdf'
        filePath = os.path.join(path,  filename) # path to save the PDF file
        print(url_link)
        print(filePath)
        PDFDownloader(url=url_link, filePath=filePath)
    print('finished downloading pdfs for ' + rest_name)


# Download PDFs with Selenium
def java_PDF(rest_name, url, prex=None, link_=True, xpath_=None):
    path = create_folder(rest_name, folder)
    s = Service(web_browser_path)
    browser = webdriver.Chrome(service=s)
    browser.get(url)
    # links that contain PDF
    if link_:
        links = [link.get_attribute('href') for link in
                 browser.find_elements(by=By.PARTIAL_LINK_TEXT, value='Download')]
    else:
        links = [link.get_attribute('href') for link in
                 browser.find_elements(by=By.XPATH, value=xpath_)]
    for url_link in links:
        browser.get(url_link)
        sleep(5)
        if 'https://' not in url_link and 'http://' not in url_link:
            if url_link[0] != '/':
                url_link = '/' + url_link
            url_link = prex + url_link
        filename = url_link.split('/')[-1]
        if filename[-3:] != 'pdf':
            if '.pdf' in filename: 
                filename = filename.split('?')[0]
                print(filename)
            else: 
                filename = filename + '.pdf'
        filePath = os.path.join(path,  filename) # path to save the PDF file
        print(url_link)
        print(filePath)
        PDFDownloader(url=url_link, filePath=filePath)
    browser.quit()

def IMGDownloader(url, filePath):
    img_data = requests.get(url).content
    with open(filePath, 'wb') as handler:
        handler.write(img_data)

def combo_imgDownload(rest_name,url,folder):
    path = create_folder(rest_name, folder)
    s = Service(web_browser_path)
    browser = webdriver.Chrome(service=s)
    browser.get(url)
    sleep(3)
    images = browser.find_elements(by=By.XPATH, value='//img[contains(@src, "jpeg")]')
    for image in images:
        image_link = image.get_attribute("src")
        image_name = image_link.split('/')[-1]
        image_path = os.path.join(path, image_name)
        IMGDownloader(image_link,image_path)


# function: create a folder and run the spider
def RunSpider(spidername, folder, json_=False):
    '''
    This function allows the spiders to run and saves the spider outputs
    :param spidername: the name of the spider you want to run
    :param folder: folder for the data collection wave
    :param json_: Default is False (file saving as csv).
    :return: spider output saved in csv or json
    '''
    op_sys = platform.system() # for the windows system, I will use the relative path for the file storage path
    os.chdir(root_path)
    path = create_folder(spidername, folder) # create a folder for the spider output
    os.chdir('./Scrapy_spiders')
    if op_sys == 'Windows': 
        if json_:
            json_file_name = spidername + '_items.json'
            json_file_path = os.path.join(path, json_file_name)
            os.system("scrapy crawl " + spidername + " -o ..\\" + json_file_path)
            with open('..\\' + json_file_path,'r') as jsonfile:
                json_data = json.load(jsonfile)
            json_df = pd.DataFrame(json_data)
            json_df.to_csv(json_file_path.replace('.json', '.csv'), index=False)
        else:
            csv_file_name = spidername + '_items.csv'
            csv_file_path = os.path.join(path, csv_file_name)
            os.system("scrapy crawl " + spidername + " -o ..\\" + csv_file_path)
    else: 
        if json_:
            json_file_name = spidername + '_items.json'
            json_file_path_root = os.path.join(root_path, path, json_file_name)
            os.system("scrapy crawl " + spidername + " -o" + json_file_path_root)
            with open(json_file_path_root,'r') as jsonfile:
                json_data = json.load(jsonfile)
            json_df = pd.DataFrame(json_data)
            json_df.to_csv(json_file_path_root.replace('.json', '.csv'), index=False)
        else:
            csv_file_name = spidername + '_items.csv'
            csv_file_path_root = os.path.join(root_path, path, csv_file_name)
            os.system("scrapy crawl " + spidername + " -o " + csv_file_path_root)
    os.chdir(root_path)
    print('finished scraping ' + spidername)

# function: run the script for a restaurant (requests)
def RunScript(rest_name):
    try:
        os.system('python ' + rest_name + '.py')
        print('Successfully scraped ' + rest_name)
    except:
        print('Issues with' + rest_name + '. Please Review')

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
                path_temp = os.path.join(path, url_pdf.split('/')[-1]) # path to save the PDF file
                PDFDownloader(url_pdf, path_temp)
