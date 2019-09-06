import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from logzero import logger

HOME_URL='https://www.nankankeiba.com/'

def get_uma_csv():
   race_list_link_list = ['program/00000000000000.do']# TODO use method
   unique_uma_link_list = []
   df = pd.DataFrame()
   for link in race_list_link_list:
      race_link_list = get_race_link_list_from_race_list_link(link)
      logger.info(race_link_list)

   for link in race_link_list:
      uma_link_list = get_uma_link_list_from_race_link(link)
      unique_uma_link_list += list(set(uma_link_list))
   
   #logger.info(unique_uma_link_list)
  
   for link in unique_uma_link_list:
      df = pd.concat([df, get_df_from_uma_link(link)]) 
   
   #df = df.reset_index()
   df.to_csv('/code/data/keiba-ataru/uma.csv')

def url_to_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

def get_race_link_list_from_race_list_link(race_list_link):
    soup = url_to_soup(HOME_URL + race_list_link)
    race_link_list = [ link.attrs['href'] for link in soup.find_all( href=re.compile("/race_info/*"))]
    return race_link_list

def get_uma_link_list_from_race_link(race_link):
    soup = url_to_soup(HOME_URL + race_link)
    uma_link_list = [ link.attrs['href'] for link in soup.find_all( href=re.compile("/uma_info/*"))]
    return uma_link_list

def get_df_from_uma_link(uma_link):
    soup = url_to_soup(HOME_URL + uma_link)
    
    uma_nm = soup.find('h2', id='tl-prof').text
    logger.info(uma_nm)
    
    uma_info_list = soup.find_all('table', class_=re.compile('tb01*'))[4].text.replace('\n\n','').splitlines()
    logger.info('label:' + str(uma_info_list[0:18]))
    
    if len(uma_info_list)%18 != 0:
       logger.info('data from' + uma_link + 'is wrong')
       return
    uma_info_num = len(uma_info_list)//18
    
    pd_columns = ['馬名']
    pd_data = [uma_nm]
    
    df = pd.DataFrame(data=[pd_data + uma_info_list[i*18:18+i*18] for i in range(1,uma_info_num)], columns=pd_columns + uma_info_list[0:18])
    return df